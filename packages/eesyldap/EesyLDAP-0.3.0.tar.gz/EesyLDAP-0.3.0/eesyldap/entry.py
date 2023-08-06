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

from copy import deepcopy
import logging

from ldap.dn import escape_dn_chars
from ldap.dn import explode_dn

log = logging.getLogger(__name__)


class LDAPEntry:
    """
    LDAP entry

    This class abstract a LDAP entry as a Python object
    """

    # Client reference
    _client = None

    # LDAP object reference
    _obj = None

    # LDAP object DN
    _dn = None

    # LDAP attributes values
    _attrs_values = None

    # LDAP attributes new values (on changed)
    _new_attrs_values = None

    # List LDAP attributes for which we must use the replace operation on change
    _force_replace_attrs = None

    def __init__(self, client, obj, dn=None, attrs_values=None):
        self._client = client
        self._obj = obj
        self._dn = dn
        self._attrs_values = dict(
            (attr_name.lower(), attr_values)
            for attr_name, attr_values in (attrs_values or {}).items()
        )
        self._new_attrs_values = {}
        self._force_replace_attrs = []

    def copy(self):
        """ Create a copy of the current LDAPEntry object """
        new_entry = self.__class__(self._client, self._obj, dn=deepcopy(self._dn), attrs_values=deepcopy(self._attrs_values))
        new_entry._new_attrs_values = deepcopy(self._new_attrs_values)  # pylint: disable=protected-access
        new_entry._force_replace_attrs = deepcopy(self._force_replace_attrs)  # pylint: disable=protected-access
        return new_entry

    def get_values(self, attr, default=None):
        """ Get an attributes's values """
        attr = attr.lower()
        # log.debug('%s.get_values(%s) : cur = %s / new = %s', self, attr, self._attrs_values.get(attr), self._new_attrs_values.get(attr))
        return self._new_attrs_values.get(attr, self.get_original_values(attr, default=default))

    def get_original_values(self, attr, default=None):
        """ Get an attributes's orignal values """
        attr = attr.lower()
        return self._attrs_values.get(attr, default)

    def set_values(self, attr, values, force_replace=False):
        """ Set an attributes's values """
        assert isinstance(values, list) or values is None, "Entry attributes values must a list or None (%s given for attribute %s)" % (type(values), attr)
        attr = attr.lower()
        # log.debug('%s.set_values(%s, %s) : cur = %s / new = %s', self, attr, values, self._attrs_values.get(attr), self._new_attrs_values.get(attr))
        if self._new_attrs_values.get(attr):
            if values == self._new_attrs_values[attr]:
                log.debug('%s.set_values(%s, %s) : new values same as current new one', self, attr, values)
                return True
            # Try to restore current LDAP value ?
            if values == self._attrs_values.get(attr) and not force_replace:
                log.debug('%s.set_values(%s, %s) : new values same as current LDAP one => restore it', self, attr, values)
                del self._new_attrs_values[attr]
                if attr in self._force_replace_attrs:
                    self._force_replace_attrs.remove(attr)
                return True
        elif values == self._attrs_values.get(attr) and not force_replace:
            log.debug('%s.set_values(%s, %s) : new values same as current one', self, attr, values)
            return True
        self._new_attrs_values[attr] = values
        if force_replace and attr not in self._force_replace_attrs:
            self._force_replace_attrs.append(attr)
        return True

    def is_present(self, attr):
        """ Check if an attribute is present/defined """
        attr = attr.lower()
        if attr in self._new_attrs_values:
            return self._new_attrs_values[attr] is not None
        return attr in self._attrs_values

    def is_modified(self, attr=None):
        """ Check if the entry (or one of this attribute) is modified """
        return bool(self._new_attrs_values) if attr is None else (attr in self._new_attrs_values)

    def get_dn(self, new_rdn=None):
        """
        Retreive or generate LDAP object DN

        :param  new_rdn:    The LDAP entry new RDN value (ex : uid=jdoe)
        """
        if self._dn and not new_rdn:
            return self._dn

        # If new RDN is provided, compose DN with it
        if new_rdn:
            exploded_dn = explode_dn(self._dn)
            return "%s,%s" % (new_rdn, ','.join(exploded_dn[1:]))

        # Otherwise, compose DN with first RDN attribute value
        rdn_values = self.get_values(self._obj.rdn_ldap_attr)
        if not rdn_values:
            return False
        base_dn = self._client.get_object_base_dn(self._obj.__class__)
        return "%s=%s,%s" % (self._obj.rdn_ldap_attr, escape_dn_chars(rdn_values[0].decode('utf-8')), base_dn)

    def save(self):
        """ Save changes on the LDAP entry """

        # Generate old / new attrs dict (only changed attributes)
        old_attrs = {}
        new_attrs = {}
        for attr in self._new_attrs_values:
            if self._new_attrs_values[attr] is not None:
                new_attrs[attr] = self._new_attrs_values[attr]
            if attr in self._attrs_values:
                old_attrs[attr] = self._attrs_values[attr]

        rdn_attr = self._obj.rdn_ldap_attr.lower()

        if self._dn is None:
            # New object
            dn = self.get_dn()
            new_attrs['objectClass'] = [c.encode('utf8') for c in self._obj.classes]
            log.debug('Object is new : add it with DN "%s" and the following attributes : %s', dn, new_attrs)
            if self._client.add(self._obj, dn, new_attrs):
                self._saved(new_values=new_attrs, new_dn=dn)
                return True
        elif rdn_attr in new_attrs:
            # Existing LDAP entry and need to be renamed
            new_rdn = "%s=%s" % (rdn_attr, escape_dn_chars(new_attrs[rdn_attr][0].decode('utf8')))
            log.debug('The RDN of the object %s changed : rename it with new RDN "%s"', self._obj.dn, new_rdn)
            if self._client.rename(self._obj, new_rdn):
                # Set RDN attr and DN as saved
                self._saved(
                    new_values=new_attrs[rdn_attr],
                    old_values=old_attrs[rdn_attr],
                    attr=rdn_attr,
                    new_dn=self.get_dn(new_rdn=new_rdn)
                )

                # Remove RDN attr in old / new attrs
                del old_attrs[rdn_attr]
                del new_attrs[rdn_attr]
            else:
                log.debug('Fail to rename object : do not continue')
                return False

        if old_attrs or new_attrs:
            # Existing object with changes
            log.debug('%s : save() : old = %s / new = %s', self, old_attrs, new_attrs)
            if self._client.modify(self._obj, old_attrs, new_attrs, force_replace_attrs=self._force_replace_attrs):
                self._saved(new_values=new_attrs, old_values=old_attrs)
                return True
            return False

        # Existing object without changes
        log.debug('%s : save() : no changes', self._dn)
        log.debug('%s : no changes to save', self._dn)
        return True

    def _saved(self, new_values, old_values=None, new_dn=None, attr=None):
        """
        Set entry as saved

        :param  new_values:     New attributes values (only attr value if attr is set)
        :param  new_dn:         New DN (optional)
        :param  attr:           Attribute name if saved changed is about only one attribute (optional)
        """
        if new_dn:
            log.debug('Set new LDAP entry DN to "%s"', new_dn)
            self._dn = new_dn
        if attr is not None:
            log.debug('Set changed of attribute %s as saved : %s => %s', attr, old_values or 'Unknwon', new_values)
            if new_values is None:
                del self._attrs_values[attr]
            else:
                self._attrs_values[attr] = new_values
            del self._new_attrs_values[attr]
            if attr in self._force_replace_attrs:
                self._force_replace_attrs.remove(attr)
        else:
            for attr_name, attr_values in new_values.items():
                log.debug(
                    'Set changed of attribute %s as saved : %s => %s',
                    attr_name,
                    old_values.get(attr_name, 'Undefined') if old_values else 'Unknwon',
                    attr_values or 'Undefined'
                )
                self._attrs_values[attr_name] = attr_values
                if attr_name in self._new_attrs_values:
                    del self._new_attrs_values[attr_name]
                if attr_name in self._force_replace_attrs:
                    self._force_replace_attrs.remove(attr_name)
            if old_values:
                for attr_name, attr_values in old_values.items():
                    if attr_name not in new_values:
                        log.debug('Set changed of attribute %s as deleted', attr_name)
                        del self._attrs_values[attr_name]
                    if attr_name in self._new_attrs_values:
                        del self._new_attrs_values[attr_name]
                    if attr_name in self._force_replace_attrs:
                        self._force_replace_attrs.remove(attr_name)

    def restore(self):
        """ Restore LDAP entry at initial state """
        self._new_attrs_values = {}
        return True

    def __repr__(self):
        """ Compute and return the “official” string representation of the LDAPEntry """
        return "<LDAPEntry %s>" % (self._dn or '[new]')

    def __getstate__(self):
        """ Retreive the state of the LDAP entry object for pickle """
        return dict(
            _dn=deepcopy(self._dn),
            _attrs_values=deepcopy(self._attrs_values),
            _new_attrs_values=deepcopy(self._new_attrs_values),
        )

    def __setstate__(self, state):
        """ Set the state of the LDAP entry object from pickle state """
        self.__dict__.update(state)

    def serialize(self):
        """ Retreive the serialized state of the LDAP entry object """
        return self.__getstate__()

    @classmethod
    def unserialize(cls, client, obj, state):
        """ Retreived on object from it serialized state and client and objects references """
        entry = cls(client, obj)
        entry.__setstate__(state)
        return entry
