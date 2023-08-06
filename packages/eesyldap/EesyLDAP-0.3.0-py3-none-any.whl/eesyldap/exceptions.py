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

""" LDAP Exceptions """

from ldap import SIZELIMIT_EXCEEDED     # pylint: disable=no-name-in-module


class LDAPException(Exception):
    """ That is the base exception class for all the other exceptions provided by this module. """


class LDAPInvalidAttributeName(AttributeError, LDAPException):
    """ Raised when an invalid attribute is call on an LDAPObject """

    def __init__(self, attr_name):
        self.attr_name = attr_name
        super().__init__("Invalid attribute name '%s'" % attr_name)


class LDAPInvalidAttributeValue(TypeError, LDAPException):
    """ Raised when an invalid value is affected to an attribute on an LDAPObject """

    def __init__(self, attr_name, attr_value, msg=None):
        self.attr_name = attr_name
        self.attr_value = attr_value
        super().__init__(msg or "Invalid value affected to attribute '%s'" % attr_name)


class LDAPNotUniqueAttribute(TypeError, LDAPException):
    """ Raised when an attribute is call as an LDAPObject identifier
    but is not unique."""

    def __init__(self, attr_name):
        self.attr_name = attr_name
        super().__init__("Attribute %s is not unique" % attr_name)


class LDAPAttributeUnicityError(LDAPInvalidAttributeValue):
    """ Raised when try to set a value to an LDAP attribute and when this
    value is already affected to another object(s)."""

    def __init__(self, attr_name, attr_value, other_objects_dn):
        self.other_objects_dn = other_objects_dn
        super().__init__(attr_name, attr_value, msg="The value '%s' of the attribute %s is not unique. This value is already affected to the following LDAP object(s) : %s" % (attr_value.decode('utf-8'), attr_name, ', '.join(other_objects_dn)))


class LDAPRequiredAttribute(LDAPInvalidAttributeValue):
    """ Raised when an attribute is set to None while is required. """

    def __init__(self, attr_name):
        super().__init__(attr_name, None, msg="Attribute %s is required" % attr_name)


class LDAPDuplicateObjectFound(LDAPException):
    """ Raised when looking for an unique LDAPObject and multiple one found. """

    def __init__(self, obj_type, filterstr=None, base_dn=None, scope=None):
        self.obj_type = obj_type
        self.filterstr = filterstr
        self.base_dn = base_dn
        self.scope = scope
        super().__init__("Duplicated object %s found" % obj_type.__name__)


class LDAPConnectionError(LDAPException):  # pylint: disable=too-few-public-methods
    """ Raised when fail to connect/bind to LDAP server """

    def __init__(self, uri, details=None):
        self.uri = uri
        self.details = details
        super().__init__(
            "Fail to connect on LDAP server %s (detail: %s)" % (
                uri, details if details else "No detail available"
            )
        )


class LDAPInvalidCredentials(LDAPConnectionError):
    """ Raised when trying to bind on LDAP server with invalid credentials. """

    def __init__(self, uri, bind_dn):
        self.bind_dn = bind_dn
        super().__init__(uri, "Invalid credential for %s" % bind_dn)


class LDAPDuplicatedRelationName(LDAPException):
    """ Raised when trying to add a relation on with a name already affected to another relation """

    def __init__(self, obj_type, rel_name, other_rel):
        self.obj_type = obj_type
        self.rel_name = rel_name
        self.other_rel = other_rel
        super().__init__("The relation '%s' already exist (%s) on object %s" % (rel_name, other_rel, obj_type.__name__))


class LDAPRelationAttributeConflictName(LDAPException):
    """ Raised when trying to add a relation on with a name already affected to an attribute """

    def __init__(self, obj_type, rel_name, attr):
        self.obj_type = obj_type
        self.rel_name = rel_name
        self.attr = attr
        super().__init__("The relation name '%s' is already used by an attribute (%s) on object %s" % (rel_name, attr, obj_type.__name__))


class LDAPRelationLinkAttributeValueMissing(LDAPException):
    """ Raised when trying to get link value of an object and no value is retreived """

    def __init__(self, rel, obj):
        self.rel = rel
        self.obj = obj
        super().__init__("No link attribute value found for the relation %s and the object %s" % (rel, obj))


class LDAPRelatedObjectModifed(LDAPException):
    """ Raised when trying to set related objects throught a relation and a related object is modified. """

    def __init__(self, rel, obj):
        self.rel = rel
        self.obj = obj
        super().__init__("The related object %s of the relation %s is modified. Please save changes before updating the relation" % (obj, rel))


class LDAPInvalidFilterMatchRule(LDAPException):
    """ Raised when invalid match rule is passed to compose a LDAP filter string. """

    def __init__(self, match):
        self.match = match
        super().__init__("Invalid LDAP filter string match rule '%s'" % match)


class LDAPInvalidFilterLogicalOperator(LDAPException):
    """ Raised when invalid logical operator is passed to combine LDAP filter strings. """

    def __init__(self, log_op):
        self.log_op = log_op
        super().__init__("Invalid LDAP filter string logical operator '%s'" % log_op)


class LDAPSearchLimitExceeded(LDAPException):  # pylint: disable=too-few-public-methods
    """ Raised when the search limit is exeeded """

    def __init__(self, limit):
        self.limit = limit
        super().__init__("More than %s matching object(s) found on LDAP server" % limit)


class LDAPSearchHardLimitExceeded(SIZELIMIT_EXCEEDED, LDAPSearchLimitExceeded):  # pylint: disable=too-few-public-methods
    """ Raised when the search hard limit is exeeded """

    def __init__(self, limit):
        self.limit = limit
        super().__init__("More than %s result found on LDAP server" % limit)
