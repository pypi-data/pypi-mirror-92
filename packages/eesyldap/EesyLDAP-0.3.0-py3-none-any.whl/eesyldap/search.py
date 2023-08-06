#!/usr/bin/env python
# -*- coding: utf-8 -*-

# EesyLDAP -- Simple LDAP Objects mapper
# By: Benjamin Renard <brenard@easter-eggs.com>
#
# Copyright (C) 2019 Benjamin Renard, Easter-eggs
# https://gitlab.com/brenard/eesyldap
#
# This file is part of EesyLDAP.
#
# EesyLDAP is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# EesyLDAP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" LDAP search """

import copy
from collections import OrderedDict
import logging

from eesyldap.exceptions import LDAPInvalidAttributeName
from eesyldap.exceptions import LDAPNotUniqueAttribute
from eesyldap.exceptions import LDAPSearchHardLimitExceeded
from eesyldap.exceptions import LDAPSearchLimitExceeded
from eesyldap.filters import combine as combine_ldap_filter

log = logging.getLogger(__name__)


class LDAPSearch:   # pylint: disable=too-many-instance-attributes
    """
    LDAP search

    This class abstract an LDAP search as a python object emulating a list object (or dict object if key_attr is provided).
    All search parameters could be provied using constructor parameters. You also could use the filter method to specify a filter
    or the sort method to specify sort parameters.

    :param  client:         The LDAPClient object
    :param  obj_type:       The object type to search
    :param  base_dn:        The base DN of the search (optional)
    :param  filterstr:      An additionnal specific LDAP filter string (optional)
    :param  scope:          The scope of the search (optional)
    :param  limit:          Specific the maximum number of object you want to retreived (optional, default: no limit)
                            If the limit is exceeded, an LDAPSearchLimitExceeded exception will be raised.
    :param  hardlimit:      Specific the maximum number of object you want to retreived (optional, default: no limit)
                            This limit is handled by LDAP server and potentially included references. Prefer limit
                            parameter usage to avoid counting references. If the limit is exceeded, an
                            LDAPSearchHardLimitExceeded exception will be raised.
    :param  sort_by:        Sort resulting objects list by an specific attribute (optional)
    :param  sort_reverse:   If true, the sorted resulting objects is reversed (optional, only use if sort_by is defined)
    :param  sort_limit:     If the number of objects to sort if upper to the specify limit, do not sort the result (optional,
                            default: no limit).
    :param  refresh:        Set to True to be sure that result is not retreive from cache (optional, default: False)
    :param  key_attr:       Set witch attribute while be used as key (optional, conflicting with sorted search)
    :param  filters:        Dict of filters to search on (optional)
    """

    _client = None
    _obj_type = None
    _filterstrs = None
    _key_attr = None
    _refresh = None

    # Sort parameters
    _sort_by = None
    _sort_reverse = False
    _sort_limit = None

    # Limit parameter
    _limit = None

    # Hard-limit parameter
    _hardlimit = None

    # Raw LDAP search result
    __result = None

    # Objects DN list (sorted if sort is enabled)
    __obj_dns = None

    # Objects key to DN mapping (if kew_attr is defined)
    __obj_key_to_dn = None

    # Objects cache
    __objs = {}

    def __init__(self, client, obj_type, base_dn=None, filterstr=None, scope=None, limit=None, hardlimit=None,
                 sort_by=None, sort_reverse=False, sort_limit=None, key_attr=None, refresh=False, **filters):
        from eesyldap.client import LDAPClient
        assert isinstance(client, LDAPClient), "obj_type argument must be an LDAPClient object (not %s)" % client
        self._client = client
        self._obj_type = obj_type
        self._base_dn = base_dn or client.get_object_base_dn(obj_type)
        self._scope = scope or client.get_object_scope(obj_type)
        self._refresh = bool(refresh)

        # Handle filters
        self._filterstrs = []
        if filterstr or filters:
            self.filter(filterstr=filterstr, **filters)

        # Handle limit/hardlimit parameters
        assert limit is None or isinstance(limit, int)
        self._limit = limit
        assert hardlimit is None or isinstance(hardlimit, int)
        self._hardlimit = hardlimit

        # Handle key attribute
        if key_attr:
            if obj_type.exists(key_attr):
                # Check attribute is unique
                if not obj_type.is_unique(key_attr):
                    raise LDAPNotUniqueAttribute(key_attr)
            elif key_attr != 'dn':
                raise LDAPInvalidAttributeName(key_attr)
            self._key_attr = key_attr

        # Handle sort parameters
        if sort_by:
            self.sort(sort_by, reverse=sort_reverse, limit=sort_limit)

    def sort(self, sort_by, reverse=False, limit=None):
        """
        Set search sort parameters

        :param  sort_by:    Sort resulting objects list by an specific attribute
        :param  reverse:    If true, the sorted resulting objects is reversed (optional, default: False)
        :param  limit:      If the number of objects to sort if upper to the specify limit, do not sort the
                            result (optional, default: no limit).
        """
        assert self._key_attr is None, "You could not sort search with key attribute defined"
        if sort_by != 'dn' and not self._obj_type.exists(sort_by):
            raise LDAPNotUniqueAttribute(sort_by)

        self._sort_by = sort_by
        self._sort_reverse = bool(reverse)
        if limit is not None:
            assert isinstance(limit, int)
            self._sort_limit = limit
        else:
            self._sort_limit = self._client.get_config('sort.limit', obj_type=self._obj_type)
        self._clear_sort_result()

    def filter(self, *filterstrs, filterstr=None, log_op=None, **filters):
        """
        Set additionnal search filters

        :param  filterstr:          LDAP filter string
        :param  filterstrs:         List of LDAP filter strings
        :param  filters:            Dict of filter attributes
        :param  log_op:             Logical operator use to combine provided fitler with existing
                                    ones (optional, default: and)
        """
        log_op = 'and' if log_op is None else log_op
        assert filterstr or filterstrs or filters, "You must provided at least one filter"
        if filterstr:
            self._filterstrs.append(filterstr)
        self._filterstrs.extend(filterstrs)
        for (attr_name, attr_value) in filters.items():
            self._filterstrs.append(self._obj_type.get_attribute_filter(attr_name, attr_value))

        # If log_op is not and/&, we need to combine filter strings. Otherwise, it will be done before search
        if log_op != 'and' and log_op != '&' and len(self._filterstrs) > 1:
            # Sort filter strings before combined it to maximum the chance to retreived
            # always the same filter string (usefull for caching key)
            self._filterstrs = [combine_ldap_filter(log_op, *sorted(self._filterstrs))]
        self._clear_result()

    def _get_filterstr(self):
        """ Return the LDAP filter string of the search """
        # Sort filter strings before combined it to maximum the chance to retreived
        # always the same filter string (usefull for caching key)
        return self._obj_type.get_filter(*sorted(self._filterstrs))

    def __getattr__(self, name):
        """ Get specific attribute value """
        if name in ['obj_type', 'client']:
            return getattr(self, "_" + name)
        if name in ['base_dn', 'scope', 'key_attr', 'refresh', 'sort_by', 'sort_reverse', 'sort_limit', 'limit', 'hardlimit']:
            return copy.copy(getattr(self, "_" + name))
        if name == 'filterstr':
            return self._get_filterstr()
        raise AttributeError("%s object has no %s attribute" % (self.__class__.__name__, name))

    def _clear_result(self):
        """ Clear result """
        self.__result = None
        self.__objs = {}
        self.__obj_key_to_dn = None
        self._clear_sort_result()

    def _clear_sort_result(self):
        """ Clear sort result """
        self.__obj_dns = None

    def _execute(self, refresh=False):
        """
        Execute prepared search

        :param  refresh:    Force refresh mode (do not retreived informations from cache or local search result)
        """
        # Check if search is already exeeded (and not refresh mode)
        if isinstance(self.__result, OrderedDict) and not refresh:
            return True

        # Clear result
        self._clear_result()

        # Check if result is in cache (if enabled and not refresh mode)
        self.__result = self._client.get_cached_object_search(
            self._obj_type,
            self.filterstr,
            self._base_dn,
            self._scope,
            refresh=refresh or self._refresh
        )

        if isinstance(self.__result, OrderedDict):
            # Ensure hard limit is not exceeded
            if self._hardlimit and len(self.__result) > self._hardlimit:
                raise LDAPSearchHardLimitExceeded(self._hardlimit)
            # Ensure limit is not exceeded
            if self._limit and len(self.__result) > self._limit:
                raise LDAPSearchLimitExceeded(self._limit)
        else:
            # Search matching objects in LDAP
            log.debug('Execute LDAP search')
            filterstr = self._get_filterstr()
            self.__result = self._client.raw_search(
                filterstr,
                base_dn=self._base_dn,
                scope=self._scope,
                attrlist=self._obj_type.ldap_attr_names(),
                limit=self._limit,
                hardlimit=self._hardlimit
            )

            # Ensure search result is an OrderedDict
            if not isinstance(self.__result, OrderedDict):
                # Otherwise, return the raw result of the search
                return self.__result

            if self.__result:
                log.debug('%s matching %s object(s) found in LDAP', len(self.__result), self._obj_type.__name__)
                # Add search result in cache (only if not empty)
                self._client.add_cached_object_search(
                    self._obj_type,
                    filterstr,
                    self._base_dn,
                    self._scope,
                    self.__result
                )
            else:
                log.debug('No %s matching object found in LDAP', self._obj_type.__name__)

        # If key attribute is defined, generate key to DN mapping
        if self._key_attr:
            self.__obj_key_to_dn = dict()
            for obj_dn, obj_attrs_values in self.__result.items():
                key = self._obj_type.get_python_attribute_value(self._key_attr, obj_attrs_values)
                assert key not in self.__obj_key_to_dn, 'Duplicated object key value "%s"' % key
                self.__obj_key_to_dn[key] = obj_dn
        return True

    def _sort(self):
        """ Sort search result (if enabled and sort limit is not exceeded) """

        # Check if result is already sorted
        if isinstance(self.__obj_dns, list):
            return True

        # Check if search is not executed
        if self.__result is None:
            return False

        if self._sort_by:
            # Check if sorted search result is in the cache
            self.__obj_dns = self._client.get_cached_object_sorted_search(
                self._obj_type,
                self.filterstr,
                self._base_dn,
                self._scope,
                self._sort_by,
                self._sort_reverse,
                refresh=self._refresh
            )

            # Otherwise, sort the search result
            if not self.__obj_dns:
                if self._sort_limit:
                    if len(self.__result) > self._sort_limit:
                        log.debug('Sort limit exceeded (%s / %s): do not sort result by %s', len(self.__result), self._sort_limit, self._sort_by)
                        self.__obj_dns = list(self.__result)
                    else:
                        log.debug('Sort limit not exceeded (%s / %s): sort result by %s', len(self.__result), self._sort_limit, self._sort_by)
                else:
                    log.debug('Sort search result by %s', self._sort_by)

                if not self.__obj_dns:
                    # Define method use as sorted() key parameter to sort search result
                    def _sort_by(obj_dn):
                        if self._sort_by == 'dn':
                            return obj_dn
                        return self._obj_type.get_python_attribute_value(self._sort_by, self.__result[obj_dn], sortable=True)
                    self.__obj_dns = list(self.__result)
                    self.__obj_dns = sorted(self.__obj_dns, key=_sort_by, reverse=self._sort_reverse)
                    self._client.add_cached_object_sorted_search(
                        self._obj_type,
                        self.filterstr,
                        self._base_dn,
                        self._scope,
                        self._sort_by,
                        self._sort_reverse,
                        self.__obj_dns
                    )
        else:
            self.__obj_dns = list(self.__result)
        return True

    def get_object_by_dn(self, obj_dn):
        """ Retreive an object of the search result by it DN """
        # Ensure search is runned and object is in the result
        if not self._execute():
            return None
        assert obj_dn in self.__result

        # Create object if not exists
        if obj_dn not in self.__objs:
            self.__objs[obj_dn] = self._obj_type(self._client, dn=obj_dn, attrs_values=self.__result[obj_dn])

        return self.__objs[obj_dn]

    def contains(self, obj_dn):
        """ Check if an object is contained in search result by its DN """
        # Ensure search is runned and object is in the result
        if not self._execute():
            return None
        return obj_dn in self.__result

    def __len__(self):
        """ Get search result length """
        if not self._execute():
            return 0
        return len(self.__result)

    def __bool__(self):
        """ Check is result is empty or not """
        if not self._execute():
            return False
        return bool(self.__result)

    def __getitem__(self, key):
        """ Get an item of the result """
        log.debug('%s.__getitem__(%s)', self, key)
        if not self._execute() or not self._sort():
            return None
        if self._key_attr:
            # Behave like a dict
            if key not in self.__obj_key_to_dn:
                raise IndexError(key)
            obj_dn = self.__obj_key_to_dn[key]
        else:
            # Behave like a list
            if isinstance(key, int):
                if key < 0:
                    # Handle negative indices
                    key += len(self)

                if key < 0 or key >= len(self):
                    # Invalid indice
                    raise IndexError('The index ({0}) is out of range.'.format(key))

                obj_dn = self.__obj_dns[key]
            elif isinstance(key, slice):
                return [self[i] for i in range(*key.indices(len(self)))]
            else:
                raise TypeError('Invalid argument type.')

        return self.get_object_by_dn(obj_dn)

    def __iter__(self):
        """ Iter on search result """
        if self._execute() and self._sort():
            for obj_dn in self.__obj_dns:
                if self._key_attr:
                    # Behave like a dict : return the key
                    if self._key_attr == 'dn':
                        yield obj_dn
                    else:
                        yield self._obj_type.get_python_attribute_value(self._key_attr, self.__result[obj_dn])
                else:
                    # Behave like a list : return the object
                    yield self.get_object_by_dn(obj_dn)

    def first(self):
        """ Retreive first object """
        if not self._execute() or not self._sort():
            return None
        obj_dn = self.__obj_dns[0]
        return self.get_object_by_dn(obj_dn)

    def keys(self):
        """ Retreive results keys """
        if not self._execute() or not self._sort():
            return None
        if self._key_attr:
            # Behave like a dict : return list of the keys
            return list(self)
        # List do not implement keys() method : return the index range
        return range(len(self))

    def items(self):
        """ Retreived search result items (as a dict) """
        # Behave like a dict : return list of tuple(key, obj)
        return [(key, self[key]) for key in self.keys()]

    def __repr__(self):
        """ Compute and return the “official” string representation of a LDAPSearch object """
        return '<LDAPSearch on %s objects with filter "%s" on base DN %s (scope=%s). State = %s>' % (
            self._obj_type.__name__,
            self.filterstr,
            self._base_dn,
            self._scope,
            ("Executed with %s result(s)" % len(self)) if isinstance(self.__result, OrderedDict) else 'Not executed'
        )
