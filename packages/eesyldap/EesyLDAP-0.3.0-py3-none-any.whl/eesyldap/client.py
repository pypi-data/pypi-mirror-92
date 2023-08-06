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

""" LDAP Client """

from collections import OrderedDict
import logging

from beaker.cache import Cache
from beaker.util import parse_cache_config_options
import ldap.modlist
from ldap import LDAPError  # pylint: disable=no-name-in-module

from eesyldap.connection import LDAPConnection
from eesyldap.exceptions import LDAPDuplicateObjectFound
from eesyldap.exceptions import LDAPInvalidAttributeName
from eesyldap.exceptions import LDAPNotUniqueAttribute
from eesyldap.exceptions import LDAPSearchLimitExceeded
from eesyldap.helpers import format_modlist
from eesyldap.object import LDAPObject
from eesyldap.search import LDAPSearch

log = logging.getLogger(__name__)


class LDAPClient:
    """
    LDAP client

    This class abstract all interactions with this LDAP server.
    """

    def __init__(self, config, **kwargs):
        """
        LDAP Client constructor

        :param  config:     LDAP client configuration

        All keyword arguments starting by 'cache_' will be used to configure Beaker object cache.
        See Beaker documentation for more details : https://beaker.readthedocs.io/en/latest/configuration.html#configuration
        """
        self.config = config

        # Cache
        self.__cache = {}
        self.cache_params = parse_cache_config_options(dict(
            ('cache.{0}'.format(k[6:]), v)
            for k, v in kwargs.items()
            if k.startswith('cache_')
        ))

        self.con = LDAPConnection(config)

    #
    # Cache helpers
    #
    def _get_cache(self, cache_namespace):
        """ Retreive/initialize cache (if enabled) for a specific namespace """
        if self.cache_params.get('enabled'):
            try:
                return self.__cache[cache_namespace]
            except KeyError:
                self.__cache[cache_namespace] = cache = Cache(cache_namespace, **self.cache_params)
                log.info('[LDAP] Cache %s enabled, type=%s, expire=%s.', cache_namespace, self.cache_params.get('type'), self.cache_params.get('expire'))
                return cache
        else:
            log.debug('[LDAP] Cache is disabled.')
        return None

    #
    # Object cache
    #
    # This cache permit to store object's data.
    #
    def _get_object_cache(self, obj_type):
        """ Return object type cache namespace """
        return self._get_cache("ldap.objects.%s" % obj_type.__name__)

    @staticmethod
    def get_cached_object_identifiers(obj):
        """
        Retreive all object identifier based on all unique attribute attr_values

        :param obj:             The object
        """

        identifiers = {'dn': obj.dn}
        for attr_name, attr_value in obj.items():
            if obj.is_unique(attr_name) and attr_value:
                identifiers[attr_name] = str(attr_value)
        return identifiers

    @staticmethod
    def get_object_cache_key(identifier, value):
        """
        Retrieve objects cache key

        :param identifier:     The LDAP object identifier attribute name
        :param value:          The LDAP object identifier attribute value
        """
        return '{0}={1}'.format(identifier, value)

    def add_cached_object(self, obj_type, obj):
        """
        Add on object in cache (if enabled)

        :param obj_type:       The object type
        :param obj:            The object
        """
        cache = self._get_object_cache(obj_type)
        if not cache:
            return

        identifiers = self.get_cached_object_identifiers(obj)

        serialized_obj = obj.serialize()
        for identifier, value in identifiers.items():
            if value:
                cache_key = self.get_object_cache_key(identifier, value)
                cache[cache_key] = serialized_obj
                log.debug('Object %s added to cache %s with key "%s" : %s', obj, cache, cache_key, serialized_obj)

    def get_cached_object(self, obj_type, identifiers=None, refresh=False):
        """
        Retrieve on object from cache (if enabled)

        :param obj_type:       The object type
        :param identifiers:    A dict of the object identifier(s) :
                                - key : the attribute name
                                - value : the value of this attribute that refer only
                                to this specific object.
        :param refresh:        Helper : force cache update if True
        """
        cache = self._get_object_cache(obj_type)
        if cache and not refresh:
            for identifier, value in identifiers.items():
                if not value:
                    continue
                cache_key = self.get_object_cache_key(identifier, value)
                try:
                    serialized_obj = cache[cache_key]
                    obj = obj_type.unserialize(self, serialized_obj)
                    log.debug('%s object %s retreived from cache %s (from key = "%s")', obj_type.__name__, obj, cache, cache_key)
                    return obj
                except KeyError:
                    pass
            log.debug('No object %s found in cache %s with identifiers %s', obj_type.__name__, cache, ' / '.join(['%s=%s' % (attr_name, attr_value) for attr_name, attr_value in identifiers.items()]))
        return None

    def delete_cached_object(self, obj_type, obj=None, identifiers=None):
        """
        Delete on object in cache (if enabled and if object is present)

        :param obj_type:       The object type
        :param obj:            The object to delete in cache (to retreive it's identifiers, see get_cached_object())
        :param identifiers:    A dict of the object identifier(s) (see get_cached_object())
        """
        cache = self._get_object_cache(obj_type)
        if not cache:
            return

        if obj is not None:
            identifiers = self.get_cached_object_identifiers(obj)

        for identifier, value in identifiers.items():
            if not value:
                continue
            cache_key = self.get_object_cache_key(identifier, value)
            try:
                del cache[cache_key]
                log.debug('Object %s removed in cache %s with key "%s"', obj, cache, cache_key)
            except KeyError:
                log.debug('Object %s not found in cache %s with key "%s"', obj, cache, cache_key)

    #
    # Object search cache
    #
    # This cache permit to store search result data as retreived from LDAPConnection.search().
    #
    def _get_object_search_cache(self, obj_type):
        """ Return search of object type cache namespace """
        return self._get_cache("ldap.objects.search.%s" % obj_type.__name__)

    @staticmethod
    def get_object_search_cache_key(filterstr, base_dn, scope):
        """
        Retrieve objects search cache key

        :param filterstr:      The LDAP search filter
        :param base_dn:        The LDAP search base DN
        :param scope:          The LDAP search scope
        """
        return 'filter={0}|base_dn={1}|scope={2}'.format(filterstr, base_dn, scope)

    def add_cached_object_search(self, obj_type, filterstr, base_dn, scope, search_result):
        """
        Add objects search in cache (if enabled)

        :param obj_type:       The object type
        :param filterstr:      The LDAP search filter
        :param base_dn:        The LDAP search base DN
        :param scope:          The LDAP search scope
        :param search_result:  The LDAP search result
        """
        cache = self._get_object_search_cache(obj_type)
        if cache:
            cache_key = self.get_object_search_cache_key(filterstr, base_dn, scope)
            cache[cache_key] = search_result
            log.debug('Object %s search added to cache %s with key "%s" (%s object(s))', obj_type.__name__, cache, cache_key, len(search_result))

    def get_cached_object_search(self, obj_type, filterstr, base_dn, scope, refresh=False):
        """
        Retrieve objects search from cache (if enabled)

        :param obj_type:       The object type
        :param filterstr:      The LDAP search filter
        :param base_dn:        The LDAP search base DN
        :param scope:          The LDAP search scope
        :param refresh:        Helper : force cache update if True
        """
        cache = self._get_object_search_cache(obj_type)
        if cache and not refresh:
            cache_key = self.get_object_search_cache_key(filterstr, base_dn, scope)
            try:
                result = cache[cache_key]
                log.debug('Search result of objects %s retreived from cache %s (with key "%s")', obj_type.__name__, cache, cache_key)
                return result
            except KeyError:
                pass
            log.debug('Search result of objects %s not found in cache %s (with key "%s")', obj_type.__name__, cache, cache_key)
        return None

    def delete_cached_object_search(self, obj_type):
        """
        Delete all objects search of a specific type in cache (if cache is enabled)

        :param obj_type:       The object type
        """
        cache = self._get_object_search_cache(obj_type)
        if cache:
            cache.clear()
            log.debug('Object %s search cache %s cleared', obj_type.__name__, cache)

        # Also delete sorted search results
        self.delete_cached_object_sorted_search(obj_type)

    #
    # Object sorted search cache
    #
    # This cache permit to store sorted search result as a list of sorted objects's DN.
    #
    def _get_object_sorted_search_cache(self, obj_type):
        """ Return sorted search of object type cache namespace """
        return self._get_cache("ldap.objects.search.%s.sorted" % obj_type.__name__)

    @staticmethod
    def get_object_sorted_search_cache_key(filterstr, base_dn, scope, sort_by, sort_reverse):
        """
        Retrieve objects sorted search cache key

        :param filterstr:      The LDAP search filter
        :param base_dn:        The LDAP search base DN
        :param scope:          The LDAP search scope
        :param sort_by:        The sort by parameter
        :param sort_reverse:   The sort reverse parameter
        """
        return 'filter={0}|base_dn={1}|scope={2}|sort_by={3}|sort_reverse={4}'.format(filterstr, base_dn, scope, sort_by, bool(sort_reverse))

    def add_cached_object_sorted_search(self, obj_type, filterstr, base_dn, scope, sort_by, sort_reverse, obj_dns):
        """
        Add objects sorted search result in cache (if enabled)

        :param obj_type:       The object type
        :param filterstr:      The LDAP search filter
        :param base_dn:        The LDAP search base DN
        :param scope:          The LDAP search scope
        :param obj_dns:        The objects's DN list
        """
        cache = self._get_object_sorted_search_cache(obj_type)
        if cache:
            cache_key = self.get_object_sorted_search_cache_key(filterstr, base_dn, scope, sort_by, sort_reverse)
            cache[cache_key] = obj_dns
            log.debug('Object %s sorted search result added to cache %s with key "%s" (%s object(s))', obj_type.__name__, cache, cache_key, len(obj_dns))

    def get_cached_object_sorted_search(self, obj_type, filterstr, base_dn, scope, sort_by, sort_reverse, refresh=False):
        """
        Retrieve objects sorted search result from cache (if enabled)

        :param obj_type:       The object type
        :param filterstr:      The LDAP search filter
        :param base_dn:        The LDAP search base DN
        :param scope:          The LDAP search scope
        :param sort_by:        The sort by parameter
        :param sort_reverse:   The sort reverse parameter
        :param refresh:        Helper : force cache update if True
        """
        cache = self._get_object_sorted_search_cache(obj_type)
        if cache and not refresh:
            cache_key = self.get_object_sorted_search_cache_key(filterstr, base_dn, scope, sort_by, sort_reverse)
            try:
                result = cache[cache_key]
                log.debug('Sorted search result of objects %s retreived from cache %s (with key "%s")', obj_type.__name__, cache, cache_key)
                return result
            except KeyError:
                pass
            log.debug('Sorted search result of objects %s not found in cache %s (with key "%s")', obj_type.__name__, cache, cache_key)
        return None

    def delete_cached_object_sorted_search(self, obj_type):
        """
        Delete all objects sorted search of a specific type in cache (if cache is enabled)

        :param obj_type:       The object type
        """
        cache = self._get_object_sorted_search_cache(obj_type)
        if cache:
            cache.clear()
            log.debug('Object %s sorted search cache %s cleared', obj_type.__name__, cache)

    #
    # Config helpers
    #
    def get_config(self, var_name, obj_type=None, default=None):
        """
        Retreive configure variable value

        :param  var_name:   The configuration variable name
        :param  obj_type:   The object type (optional). If defined, we first try to retreive the variable value
                            by prefixing it name by the object type name (in lowercase).
                            Example : for variable 'base_dn' of object type User, we first try to retreive
                            the variable 'user.base_dn'.
        :param  default:    The default value to return if variable is not defined (optinal, default: None)
        """
        if obj_type:
            return self.config.get('%s.%s' % (obj_type.__name__.lower(), var_name), self.get_config(var_name, default=default))
        return self.config.get(var_name, default)

    #
    # Objects access helpers
    #

    def get_object_base_dn(self, obj_type):
        """ Return LDAP search base DN for a specific object type """
        return self.get_config('base_dn', obj_type=obj_type)

    def get_object_scope(self, obj_type):
        """ Return LDAP search scope for a specific object type """
        return self.get_config('scope', obj_type=obj_type, default='sub')

    def get(self, obj_type, refresh=False, **identifiers):
        """
        Get an object in LDAP

        :param  obj_type:       The object type to search
        :param  refresh:        Set to True to be sure that result is not retreive from cache
        :param  identifiers:    Dict of object identifiers
        """

        # Check if object is already in cache (if enabled and not refresh mode)
        cached_object = self.get_cached_object(obj_type, identifiers=identifiers, refresh=refresh)
        if cached_object:
            return cached_object

        # Build object search parameters
        filterstr = None
        base_dn = self.get_object_base_dn(obj_type)
        scope = self.get_object_scope(obj_type)
        if identifiers.get('dn'):
            filterstr = obj_type.get_filter()
            base_dn = identifiers.get('dn')
            scope = 'base'
        elif identifiers:
            # Check identifiers
            for attr_name, attr_value in identifiers.items():
                if obj_type.exists(attr_name):
                    # Check attribute is unique
                    if not obj_type.is_unique(attr_name):
                        raise LDAPNotUniqueAttribute(attr_name)
                    filterstr = obj_type.get_attribute_filter(attr_name, attr_value)
                    break
                if attr_name != 'dn':
                    raise LDAPInvalidAttributeName(attr_name)
        if filterstr is None:
            raise Exception('No identifier specify')

        # Search matching object in LDAP
        try:
            search = self.search(
                obj_type,
                base_dn=base_dn,
                filterstr=filterstr,
                scope=scope,
                limit=1,
                refresh=refresh
            )
            if search:
                obj = search[0]
            else:
                log.debug('No matching %s object found.', obj_type.__name__)
                return None
        except LDAPSearchLimitExceeded:
            raise LDAPDuplicateObjectFound(obj_type, filterstr, base_dn, scope)

        if isinstance(obj, LDAPObject):
            log.debug('One corresponding %s object found in LDAP : %s', obj_type.__name__, obj)
            self.add_cached_object(obj_type, obj)
            return obj

        return None

    def raw_search(self, filterstr, base_dn=None, scope=None, attrlist=None, limit=None, hardlimit=None):
        """
        Run raw search using LDAP Connection and return OrderedDict with object DN as key and a dict of LDAP attributes
        values as correponding value.

        :param  filterstr:      The LDAP filter string
        :param  base_dn:        The base DN of the search (optional, default = directory base DN)
        :param  scope:          The scope of the search (optional, default: see LDAPConnection._get_scope())
        :param  attrlist:       The list of requested attributes (optional, default: all)
        :param  limit:          Specific the maximum number of object you want to retreived (optional, default: no limit)
                                If the limit is exceeded, an LDAPSearchLimitExceeded exception will be raised.
        :param  hardlimit:      Specific the maximum number of object you want to retreived (optional, default: no limit)
                                This limit is handled by LDAP server and potentially included references. Prefer limit
                                parameter usage to avoid counting references. If the limit is exceeded, an
                                LDAPSearchHardLimitExceeded exception will be raised.
        """
        base_dn = self.get_config('base_dn') if base_dn is None else base_dn
        with self.con:
            try:
                result = self.con.search(
                    base=base_dn,
                    filterstr=filterstr,
                    scope=scope,
                    attrlist=attrlist,
                    limit=limit,
                    hardlimit=hardlimit
                )
            except LDAPSearchLimitExceeded as err:
                raise err
            except Exception:
                log.error('Error occured searching with filter %s on %s (scope = %s)', filterstr, base_dn, scope, exc_info=1)
                return False

        if not result:
            log.debug('No object found in LDAP with filter %s on %s (scope = %s, attrs = %s)', filterstr, base_dn, scope, attrlist)
            return OrderedDict()

        return OrderedDict(
            (obj_dn, obj_attrs_values)
            for obj_dn, obj_attrs_values in result
        )

    def search(self, obj_type, **kwargs):
        """
        Search objects in LDAP

        This method return an LDAPSearch object.
        """
        return LDAPSearch(self, obj_type, **kwargs)

    def new(self, obj_type, attrs=None, save=False):
        """
        Create new object

        :param  obj_type:       The object type to create
        :param  attrs:          The attributes values to set on new obj (optional)
        :param  save:           Directly save or not this new obj on LDAP directory (only if attrs is provided)
        """
        obj = obj_type(self)
        if isinstance(attrs, dict):
            obj.update(attrs, save=save)
        return obj

    def modify(self, obj, old_attrs, new_attrs, force_replace_attrs=None):
        """
        Modify an object in LDAP directory

        :param  obj:                    The modified object
        :param  old_attrs:              Dict of old LDAP attributes values
        :param  new_attrs:              Dict of the LDAP attributes values
        :param  force_replace_attrs:    List LDAP attributes for which we must use the replace operation on change
        """
        # Generate ignored attributes list
        ignored_attrs = obj.protected_attrs if obj.protected_attrs else []

        # Ignore all force replace attributes (if present in new attributes and not empty)
        if force_replace_attrs:
            for attr in force_replace_attrs:
                if attr in new_attrs and new_attrs[attr]:
                    ignored_attrs.append(attr)

        # Generate modlist
        modlist = ldap.modlist.modifyModlist(
            old_attrs, new_attrs,
            ignore_attr_types=ignored_attrs
        )

        # Add replace operations for force replace attributes (if present in new attributes and not empty)
        if force_replace_attrs:
            for attr in force_replace_attrs:
                if attr in new_attrs and new_attrs[attr]:
                    modlist.append(
                        (ldap.MOD_REPLACE, attr, new_attrs[attr])  # pylint: disable=no-member
                    )

        if not modlist:
            log.debug('No change detected on object %s', obj.dn)
            return True
        log.debug(
            'LDAP changes detected on object %s :\n%s',
            obj.dn, format_modlist(modlist, prefix='  ')
        )

        # Update object in LDAP
        with self.con:
            try:
                self.con.modify(obj.dn, modlist)
                log.debug('Object %s updated in LDAP', obj.dn)
                self.delete_cached_object(obj.__class__, obj)
                self.delete_cached_object_search(obj.__class__)
                return True
            except LDAPError:
                log.error("Error updating %s : %s", obj.dn, modlist, exc_info=1)
        return False

    def rename(self, obj, new_rdn):
        """
        Modify an object in LDAP directory

        :param  obj:            The modified object
        :param  new_rdn:        The LDAP object new RDN (ex : "uid=jdoe")
        """

        # Rename object in LDAP
        with self.con:
            try:
                self.con.rename(obj.dn, new_rdn)
                log.debug('Object %s renamed in LDAP as %s', obj.dn, new_rdn)
                self.delete_cached_object(obj.__class__, obj)
                self.delete_cached_object_search(obj.__class__)
                return True
            except LDAPError:
                log.error("Error renaming %s as %s", obj.dn, new_rdn, exc_info=1)
        return False

    def add(self, obj, dn, attrs):
        """
        Add an object in LDAP directory

        :param  obj:    The object to add
        """
        with self.con:
            try:
                modlist = ldap.modlist.addModlist(attrs)
                if self.con.add(dn, modlist):
                    log.debug('Object %s added in LDAP', dn)
                    self.delete_cached_object_search(obj.__class__)
                    return True
            except LDAPError:
                log.error("Error adding %s : %s", dn, modlist, exc_info=1)
        return False

    def delete(self, obj):
        """ Delete an object in LDAP directory """
        with self.con:
            try:
                dn = obj.dn
                if dn is None:
                    log.error('Fail to retreive object DN')
                    return False
                if self.con.delete(dn):
                    log.debug('Object %s deleted in LDAP', dn)
                    self.delete_cached_object(obj.__class__, obj)
                    self.delete_cached_object_search(obj.__class__)
                    return True
            except LDAPError:
                log.error("Error deleting %s", dn, exc_info=1)
        return False
