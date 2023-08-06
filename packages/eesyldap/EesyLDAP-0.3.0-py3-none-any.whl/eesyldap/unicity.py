#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods

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

""" LDAP Attributes unicity checks """

import logging

from eesyldap.exceptions import LDAPAttributeUnicityError
from eesyldap.filters import combine as combine_ldap_filter
from eesyldap.filters import compose as compose_ldap_filter

log = logging.getLogger(__name__)


class BaseUnicityCheck:
    """
    Base class for LDAP Attributes unicity checks

    This class is not supposed to be used as unicity checker (see its chidren).
    """

    def __init__(self, **kwargs):
        """
        Constructor

        This method handle keyword arguments and define corresponding object attributes (if exists).
        """
        for arg, value in kwargs.items():
            if hasattr(self, arg):
                setattr(self, arg, value)
            else:
                raise AttributeError("Invalid keyword argument %s pass to %s constructor" % (arg, self.__class__))

    def is_unique(self, client, obj, attr, value):
        """
        Check attribute value unicity

        :param  client:     The LDAPClient object
        :param  obj:        The LDAPObject object
        :param  attr:       The attribute name to check
        :param  value:      The attribute value to check
        """
        raise NotImplementedError("%s.%s" % (self.__repr__(), 'is_unique'))

    def __repr__(self):
        """ Compute and return the “official” string representation of the Unicity Check """
        return "<%s>" % type(self).__name__


class UniqueInDirectory(BaseUnicityCheck):  # pylint: disable=too-few-public-methods
    """
    LDAP attributes unicity check on all directory objects

    This unicity check that the attribute value is unique on all of the LDAP directory objects.

    By default, deplicated values are searched on all objects in the directory with the same attribute.
    You can configured other attibutes that could stores duplicated values by using the other_attributes
    constructor parameter.
    """

    # Also check unicity on other attributes
    other_attributes = []

    # Do not raise error if the duplicated value is own by the same object
    excepted_itself = True

    def is_unique(self, client, obj, attr, value):
        """
        Check attribute value unicity

        :param  client:     The LDAPClient object
        :param  obj:        The LDAPObject object
        :param  attr:       The attribute name to check
        :param  value:      The attribute value to check
        """
        return self._is_unique(client, obj, attr, value)

    def _is_unique(self, client, obj, attr, value, base_dn=None):
        """
        Real (and overriddable) implementation of the attribute value unicity check

        :param  client:     The LDAPClient object
        :param  obj:        The LDAPObject object
        :param  attr:       The attribute name to check
        :param  value:      The attribute value to check
        :param  base_dn:    The base DN of the LDAP search of duplicated values (optional, defaut : LDAPClient directory configured base DN)
        """
        filterstr, attrs = self._compose_filterstr_and_attrlist(client, obj, attr, value)
        result = client.raw_search(filterstr, attrlist=attrs, base_dn=base_dn)
        if isinstance(result, dict):
            if result and self.excepted_itself and obj.dn in result:
                del result[obj.dn]
            if not result:
                return True
            raise LDAPAttributeUnicityError(attr, value, result.keys())
        log.error('An unexpected error occured checking the unicity of the value "%s" of the attribute %s of the object %s with the check %s', value, attr.ldap_name, obj, self)
        return False

    def _compose_filterstr_and_attrlist(self, client, obj, attr, value):  # pylint: disable=unused-argument
        """
        Compose the filterstr and the attributes list of the LDAP search of duplicated values

        :param  client:     The LDAPClient object
        :param  obj:        The LDAPObject object
        :param  attr:       The attribute name to check
        :param  value:      The attribute value to check
        """
        filterstr = compose_ldap_filter(attr.ldap_name, 'equals', value.decode('utf8'))
        attrs = [attr.ldap_name]
        if self.other_attributes:
            assert isinstance(self.other_attributes, list)
            filterstrs = [filterstr]
            for other_attr in self.other_attributes:
                filterstrs.append(compose_ldap_filter(other_attr, 'equals', value.decode('utf8')))
                attrs.append(other_attr)
            filterstr = combine_ldap_filter('or', *filterstrs)
        return (filterstr, attrs)


class UniqueInSameObjectType(UniqueInDirectory):
    """
    LDAP attributes unicity check on all directory objects of the same type

    This unicity check that the attribute value is unique on all of the same type LDAP directory objects.

    This class derive from UniqueInDirectory and override the parameter of the LDAP search of duplicated
    values. Duplicated values are searched in all objects of the same type and in the same attribute.
    As with UniqueInDirectory check, you can configured other attibutes that could stores duplicated
    values by using the other_attributes constructor parameter.
    """

    def is_unique(self, client, obj, attr, value):
        """
        Check attribute value unicity

        :param  client:     The LDAPClient object
        :param  obj:        The LDAPObject object
        :param  attr:       The attribute name to check
        :param  value:      The attribute value to check
        """
        return self._is_unique(client, obj, attr, value, base_dn=client.get_object_base_dn(obj.__class__))

    def _compose_filterstr_and_attrlist(self, client, obj, attr, value):  # pylint: disable=unused-argument
        """
        Compose the filterstr and the attributes list of the LDAP search of duplicated values

        :param  client:     The LDAPClient object
        :param  obj:        The LDAPObject object
        :param  attr:       The attribute name to check
        :param  value:      The attribute value to check
        """
        filterstr, attrs = super()._compose_filterstr_and_attrlist(client, obj, attr, value)
        filterstr = obj.get_filter(filterstr=filterstr)
        return (filterstr, attrs)
