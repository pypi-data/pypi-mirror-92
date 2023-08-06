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

""" LDAP Object """

import copy
import inspect
import logging

from eesyldap.entry import LDAPEntry
from eesyldap.exceptions import LDAPDuplicatedRelationName
from eesyldap.exceptions import LDAPInvalidAttributeName
from eesyldap.exceptions import LDAPRelationAttributeConflictName
from eesyldap.filters import combine as combine_ldap_filter

log = logging.getLogger(__name__)


class LDAPObject:
    """
    LDAP object

    This class implement a python object behind a LDAP entry
    """

    # List of the LDAP objectClass
    _class = []

    # Dict of the python object attributes
    _attrs = {}

    # Reversed mapping dict of the LDAP attribute to the python object attribute
    _srtta = None

    # RDN python and LDAP attribute
    _rdn_attr = None
    _rdn_ldap_attr = None

    # Protected attributes
    # List of attributes that will never be modified.
    _protected_attrs = None

    # Relations
    _relations = {}

    # LDAPClient object reference
    _client = None

    # LDAPEntry object reference
    _entry = None

    # Iterator index
    __iter_idx = 0

    def __init__(self, client, dn=None, attrs_values=None, entry=None, serialized_state=None):
        """
        LDAP obect constructor

        :param  client:             The LDAPClient object
        :param  dn:                 The LDAP object DN (optional for new object)
        :param  attrs_values:       The LDAP object attributes's values (optional for new object)
        :param  entry:              The LDAP entry object (optional, could be specified instead of
                                    dn and attrs_values parameters)
        :param  serialized_state:   The LDAP object serialized state (optional, could be specified
                                    instead of dn and attrs_values parameters)
        """
        self._client = client
        log.debug('Instanciate new %s object with dn %s', self.__class__, dn)
        if not self._class:
            raise NotImplementedError("%s : You must defined _class attribute" % self.__class__.__name__)
        if not self._attrs:
            raise NotImplementedError("%s : You must defined _attrs attribute" % self.__class__.__name__)
        if not isinstance(self._rdn_ldap_attr, str) and not isinstance(self._rdn_attr, str):
            raise NotImplementedError("%s : You must defined _rdn_attr or _rdn_ldap_attr attribute" % self.__class__.__name__)

        # Generate reversed mapping dict of LDAP attribute to Python object attribute
        self._srtta = self._get_srtta()

        # Check RDN attribute
        self._rdn_ldap_attr = self.get_rdn_ldap_attr()
        self._rdn_attr = self.get_rdn_attr()
        if self.is_multiple(self._rdn_attr):
            raise NotImplementedError('%s : The attribute %s defined as RDN is multiple and multi-valued attribute is not yet supported as RDN' % (self.__class__.__name__, self._rdn_attr))

        # Check relations
        for rel_name in self._relations:
            # Check conflict between attribute and relation names
            if rel_name in self._attrs:
                raise LDAPRelationAttributeConflictName(self.__class__, rel_name, self._attrs[rel_name])

        # Create dedicated LDAP entry
        if isinstance(entry, LDAPEntry):
            self._entry = entry
        elif serialized_state is not None:
            self._entry = LDAPEntry.unserialize(client, self, serialized_state)
        else:
            self._entry = LDAPEntry(client, self, dn, attrs_values)

        # Iterator index
        self.__iter_idx = 0

    @classmethod
    def _get_srtta(cls):
        """ Generate reversed mapping dict of LDAP attribute to Python object attribute """
        srtta = {}
        for attr in cls._attrs:
            ldap_attr_name = cls._attrs[attr].ldap_name
            assert ldap_attr_name not in srtta, "LDAP attribute %s is affected to multiple object attributes : %s / %s" % (ldap_attr_name, srtta[ldap_attr_name], attr)
            srtta[ldap_attr_name] = attr
        return srtta

    def get_dn(self):
        """ Retreive or generate LDAP object DN """
        return self._entry.get_dn()

    def __getattr__(self, name):
        """ Get an DN or attributes's value """
        if name == 'dn':
            return self._entry.get_dn()
        if name == 'attrs':
            return LDAPObjectAttributesWrapper(self, self._attrs)
        if name == 'classes':
            return self._entry.get_values('objectClass', default=self._class)
        if name == 'entry':
            return self._entry
        if name == 'client':
            return self._client
        if name == 'protected_attrs':
            return copy.copy(self._protected_attrs) or []
        if name == 'rdn_attr':
            return copy.copy(self._rdn_attr)
        if name == 'rdn_ldap_attr':
            return copy.copy(self._rdn_ldap_attr)
        if self.exists(name):
            return self._attrs[name].get_value(self)
        if name in self._relations:
            return self._relations[name].get_related_objects(self)
        raise LDAPInvalidAttributeName(name)

    def __setattr__(self, name, value):
        """ Set an attribute value """
        if name in self._attrs:
            return self._attrs[name].set_value(self, value)
        if name in self._relations:
            return self._relations[name].set_related_objects(self, value)
        if hasattr(self, name):
            return object.__setattr__(self, name, value)
        raise LDAPInvalidAttributeName(name)

    def __iter__(self):
        return self

    def __next__(self):
        self.__iter_idx += 1
        try:
            return self._attrs.keys()[self.__iter_idx - 1]
        except IndexError:
            self.__iter_idx = 0
            raise StopIteration

    def items(self):
        """ Return LDAP object's attributes items like a dict """
        return [(attr_name, attr.get_value(self)) for attr_name, attr in self._attrs.items()]

    @classmethod
    def keys(cls):
        """ Return LDAP object's attribute names like dict().keys() """
        return cls._attrs.keys()

    @classmethod
    def ldap_attr_names(cls):
        """ Return list of the LDAP attribute names """
        return [attr.ldap_name for attr_name, attr in cls._attrs.items()]

    def __getitem__(self, key):
        return self._attrs[key].get_value(self)

    # Python 2.x compatibility
    next = __next__

    def __contains__(self, item):
        return item in self._attrs

    def __eq__(self, other):
        return self.dn == other.dn and dict(self) == dict(other)

    def is_present(self, name):
        """ Check if attribute is present/defined """
        if name in self._attrs:
            return self._attrs[name].is_present(self)
        raise LDAPInvalidAttributeName(name)

    @classmethod
    def is_unique(cls, name):
        """ Check if attribute is unique """
        if name in cls._attrs:
            return cls._attrs[name].is_unique()
        raise LDAPInvalidAttributeName(name)

    @classmethod
    def is_multiple(cls, name):
        """ Check if attribute is multiple """
        if name in cls._attrs:
            return cls._attrs[name].is_multiple()
        raise LDAPInvalidAttributeName(name)

    def is_modified(self, attr=None):
        """ Check if the object (or one of this attribute) is modified """
        return self._entry.is_modified(attr)

    @classmethod
    def exists(cls, name):
        """ Check if attribute exist """
        return name in cls._attrs

    @classmethod
    def add_relation(cls, rel_name, rel):
        """ Add a relation to the object type """
        if rel_name in cls._relations:
            if cls._relations[rel_name] == rel:
                return True
            raise LDAPDuplicatedRelationName(cls, rel_name, cls._relations[rel_name])
        if rel_name in cls._attrs:
            raise LDAPRelationAttributeConflictName(cls, rel_name, cls._attrs[rel_name])
        log.debug('Add relation %s on objects %s (%s)', rel_name, cls.__name__, rel)
        cls._relations[rel_name] = rel
        return True

    @classmethod
    def add_reverse_relations(cls):
        """ Add reverse relations """
        # Check relations
        for rel_name in cls._relations:
            cls._relations[rel_name].add_reverse_relation(cls)

    @classmethod
    def get_filter(cls, *other_filterstrs, filterstr=None, log_op=None, **filters):
        """
        Get object LDAP filter

        :param  filterstr:          A specific LDAP filter to combine with result
        :param  log_op:             The logical operator to use to combine additional filters (Default: and)
        :param  other_filterstrs:   List of filter strings
        :param  fiters:             Dict of filter attributes
        """
        filterstrs = ['(objectClass=%s)' % x for x in cls._class]
        additional_filters = []
        if filterstr:
            additional_filters.append(filterstr)
        additional_filters.extend(other_filterstrs)
        for (attr_name, attr_value) in filters.items():
            additional_filters.append(cls.get_attribute_filter(attr_name, attr_value))
        # Combine additional filters if log_op != and (default) and if we have more than one additional filters
        if len(additional_filters) > 1 and log_op is not None and log_op not in ('and', '&'):
            filterstrs.append(combine_ldap_filter(log_op, *additional_filters))
        else:
            filterstrs.extend(additional_filters)
        return combine_ldap_filter('and', *filterstrs) if len(filterstrs) > 1 else filterstrs[0]

    @classmethod
    def get_attribute_filter(cls, attr_name, attr_value=None, match=None):
        """
        Get object attribute LDAP filter string

        :param  attr_name:      The attribute name
        :param  attr_value:     The attribute value
        :param  match:          Match rule as accept by eesyldap.filters.compose (optional)
        """
        if attr_name in cls._attrs:
            return cls._attrs[attr_name].get_filter(attr_value, match=match)
        raise LDAPInvalidAttributeName(attr_name)

    @classmethod
    def get_rdn_attr(cls):
        """ Return object RDN attribute name """
        if cls._rdn_attr:
            return cls._rdn_attr
        if cls._rdn_ldap_attr:
            for attr_name, attr in cls._get_srtta().items():
                if cls._rdn_ldap_attr == attr_name:
                    cls._rdn_attr = attr
                    return attr
            raise AssertionError("Invalid LDAP attribute %s defined as RDN" % cls._rdn_ldap_attr)
        raise NotImplementedError('No RDN attribute or LDAP attribute defined')

    @classmethod
    def get_rdn_ldap_attr(cls):
        """ Return object RDN LDAP attribute name """
        if cls._rdn_ldap_attr:
            return cls._rdn_ldap_attr
        if cls._rdn_attr:
            assert cls._rdn_attr in cls._attrs, "Invalid attribute %s defined as RDN" % cls._rdn_attr
            cls._rdn_ldap_attr = cls._attrs[cls._rdn_attr].ldap_name
            return cls._rdn_ldap_attr
        raise NotImplementedError('No RDN attribute or LDAP attribute defined')

    @classmethod
    def get_python_attribute_value(cls, attr_name, ldap_attrs_values, sortable=None):
        """ Return the python value of an attribute based on specified LDAP values """
        if attr_name in cls._attrs:
            ldap_name = cls._attrs[attr_name].ldap_name.lower()
            for name, values in ldap_attrs_values.items():
                if name.lower() == ldap_name:
                    return cls._attrs[attr_name].get_value(ldap_values=values, sortable=sortable)
            # Attribute not present in LDAP values
            log.debug("Attribute %s (%s) not present in LDAP attributes's values provided (%s)", cls._attrs[attr_name], ldap_name, ldap_attrs_values)
            return cls._attrs[attr_name].get_value(ldap_values=None, sortable=sortable)
        raise LDAPInvalidAttributeName(attr_name)

    def update(self, changes=None, save=True, **to_update):
        """
        Update object attributes

        :param  changes:    Dict of changes to apply on current object
        :param  save:       Enable or disable saving changes after apply
        """
        if changes:
            assert isinstance(changes, dict), "changes parameter must be a dict"
            to_update.update(changes)

        if not to_update:
            log.debug('%s.update() : No changes', self)
            return True

        # Check changes on relations to make it only at the after saving
        changes_on_relations = {}
        for attr, value in to_update.items():
            if attr in self._relations:
                changes_on_relations[attr] = value

        if changes_on_relations and not save:
            log.error('%s : Changes on relations could only be done if save is enabled', self)
            return False

        for attr, value in to_update.items():
            if self.exists(attr):
                self.__setattr__(attr, value)
            elif attr not in changes_on_relations:
                raise LDAPInvalidAttributeName(attr)
        if save:
            if not self.save():
                return False
            # Set changes on related objects
            error = False
            for rel_name, value in changes_on_relations.items():
                if not self.__setattr__(rel_name, value):
                    error = True
            return not error
        return True

    def copy(self):
        """ Create a copy of current object """
        return self.__class__(self._client, entry=self._entry.copy())

    def save(self):
        """ Save changes on LDAP object """
        # If object have relations, keep old version of this object, before modify
        if self._relations:
            old_obj = self.copy()
            old_obj.restore()

        # Save change on LDAP entry
        if not self._entry.save():
            return False

        # If object have relation, handle changes on it relations
        if self._relations:
            error = False
            for rel_name in self._relations:
                if not self._relations[rel_name].handle_object_changes(old_obj, self):
                    error = True
            return not error
        return True

    def restore(self):
        """ Restore LDAP object at initial LDAP state """
        return self._entry.restore()

    def refresh(self):
        """ Refresh LDAP object data from LDAP """
        refreshed = self._client.get(self.__class__, dn=self.dn, refresh=True)
        if refreshed:
            self._entry = refreshed.entry
            return True
        return False

    def delete(self):
        """ Delete the LDAP object on LDAP directory """
        if not self._client.delete(self):
            return False
        if self._relations:
            error = False
            for rel_name in self._relations:
                if not self._relations[rel_name].handle_object_removal(self):
                    error = True
            return not error
        return True

    def __repr__(self):
        """ Compute and return the “official” string representation of the LDAPObject """
        return "<LDAPObject %s %s>" % (type(self).__name__, (self.dn or '[new]'))

    def serialize(self):
        """ Retreive the serialized state of the LDAP object """
        return self._entry.serialize()

    @classmethod
    def unserialize(cls, client, state):
        """ Retreived an LDAPObject from it serialized state and client object reference """
        return cls(client, serialized_state=state)


class LDAPObjectAttributesWrapper:  # pylint: disable=too-few-public-methods
    """ Wrapper on LDAP object attributes dict """

    def __init__(self, obj, attrs):
        self._obj = obj
        self._attrs = attrs

    def __getattr__(self, name):
        if name in self._attrs:
            return LDAPObjectAttributeWrapper(self._obj, self._attrs[name])
        raise LDAPInvalidAttributeName(name)


class LDAPObjectAttributeWrapper:  # pylint: disable=too-few-public-methods
    """ Wrapper on LDAP object attribute """

    def __init__(self, obj, attr):
        self.__obj = obj
        self.__attr = attr

    def __getattr__(self, name):
        if not hasattr(self.__attr, name):
            raise AttributeError("%s object as no attribute '%s'" % (self.__attr.__class__.__name__, name))
        if callable(getattr(self.__attr, name)):
            return LDAPObjectAttributeCallableWrapper(self.__obj, getattr(self.__attr, name))
        return getattr(self.__attr, name)


class LDAPObjectAttributeCallableWrapper:  # pylint: disable=too-few-public-methods
    """
    Wrapper on LDAP object attribute's callable

    This wrapper add LDAP object reference as obj parameter on call (if accepted).
    """

    def __init__(self, obj, attr_callable):
        self.__obj = obj
        self.__callable = attr_callable

    def __call__(self, *args, **kwargs):
        if 'obj' in inspect.getfullargspec(self.__callable).args:
            kwargs['obj'] = self.__obj
        return self.__callable.__call__(*args, **kwargs)
