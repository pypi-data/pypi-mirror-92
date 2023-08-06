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

""" LDAP Attributes """

import copy
import datetime
import json
import logging
import re

import dateutil.parser
import dateutil.tz
from passlib.hash import ldap_md5
from passlib.hash import ldap_md5_crypt
from passlib.hash import ldap_sha1
from passlib.hash import ldap_salted_sha1
from passlib.hash import ldap_sha256_crypt
from passlib.hash import ldap_sha512_crypt
import pytz

from eesyldap.exceptions import LDAPRequiredAttribute
from eesyldap.object import LDAPObject
from eesyldap.unicity import BaseUnicityCheck
from eesyldap.filters import combine as combine_ldap_filter
from eesyldap.filters import compose as compose_ldap_filter

log = logging.getLogger(__name__)
ldap_date_format = '%Y%m%d%H%M%SZ'


class Base:
    """
    LDAP attribute

    This class abstract a LDAP entry's attribute as a Python object
    """

    # Set to True if this attribute must be change in LDAP by using replace operation
    force_replace = False

    # Set to True if this attribute could only be write in LDAP (and never read)
    write_only = False

    def __init__(self, ldap_name, multiple=False, required=None, unicity=None, default_ldap=None, default_python=None,
                 force_replace=None, write_only=None):
        """
        Create a new LDAP attribute

        :param  ldap_name:          The LDAP attribute name
        :param  multiple:           Is it a multiple values attribute? Default: False
        :param  required:           Is it a required attribute? Default: False
        :param  unicity:            The value of this attribute must be unique (optional)
        :param  default_ldap:       The default value to set on LDAP server if this attribute is not set
        :param  default_python:     The default value to set on Python object if this attribute is not set on LDAP server
        :param  force_replace:      Set to True if this attribute must be change in LDAP by using replace operation
        :param  write_only:         Set to True if this attribute could only be write in LDAP (and never read)
        """
        self.ldap_name = ldap_name
        self.multiple = multiple
        self.required = required
        assert unicity is None or isinstance(unicity, BaseUnicityCheck)
        self.unicity = unicity
        if default_ldap is not None:
            if multiple:
                assert isinstance(default_ldap, list), "Default LDAP value of attribute with multiple values must be a list of string"
                for value in default_ldap:
                    assert isinstance(value, str), "Default LDAP value of attribute with multiple values must be a list of string"
            else:
                assert isinstance(default_ldap), "Default LDAP value must be a string"
        self.default_ldap = default_ldap
        self.default_python = [] if default_python is None and multiple else default_python

        if force_replace:
            self.force_replace = True

        if write_only:
            self.write_only = True

    def _to_python(self, value, sortable=None):
        """
        Convert attribute value from LDAP to Python

        :param  value:      The LDAP attribute value to convert
        :param  sortable:   If True, make sure that returned value is sortable with others
        """
        raise NotImplementedError("%s.%s" % (self.__repr__(), '_to_python'))

    def _to_ldap(self, value):
        """
        Convert attribute value from Python to LDAP

        :param  value:  The python attribute value to convert
        """
        raise NotImplementedError("%s.%s" % (self.__repr__(), '_to_ldap'))

    def get_value(self, obj=None, ldap_values=None, sortable=None):
        """
        Get python value from LDAP attribute

        :param  obj:            The LDAP object
        :param  ldap_values:    The LDAP attribute values
        :param  sortable:       If True, make sure that returned value is sortable with others
        """
        if not ldap_values and obj:
            ldap_values = obj.entry.get_values(self.ldap_name, default=self.default_ldap)

        if not ldap_values or self.write_only:
            if self.default_python is None and sortable:
                return [] if self.multiple else self._to_python(None, sortable=True)
            return self.default_python

        if self.multiple:
            return [self._to_python(value, sortable=sortable) for value in ldap_values]
        return self._to_python(ldap_values[0], sortable=sortable)

    def set_value(self, obj, value, force_replace=False):
        """
        Set LDAP value from python

        :param  obj:            The LDAP object
        :param  value:          The new attribute python value
        :param  force_replace:  Force using LDAP replace operation on change
        """
        assert (isinstance(value, list) or value is None) or not self.multiple, "%s : Multiple attribute value must be a list" % self.ldap_name
        if value is None and self.required:
            raise LDAPRequiredAttribute(self.ldap_name)
        if not self.write_only and value == self.get_value(obj):
            log.debug('%s : set value is same as current one', self.ldap_name)
        else:
            log.debug('%s : set new values to %s', self.ldap_name, value)
            if value is None:
                if self.default_ldap is not None:
                    new_values = self.default_ldap if self.multiple and (isinstance(self.default_ldap, list) or self.default_ldap is None) else [self.default_ldap]
                else:
                    new_values = None
            elif self.multiple:
                new_values = [self._to_ldap(v) for v in value]
            else:
                new_values = [self._to_ldap(value)]
            log.debug('%s : set raw new values to %s', self.ldap_name, new_values)
            if self.is_unique() and new_values is not None:
                original_values = obj.entry.get_original_values(self.ldap_name, default=[])
                for new_value in new_values:
                    if new_value in original_values:
                        #  Don't check original values of the entry (that will be only restored)
                        continue
                    if not self.unicity.is_unique(obj.client, obj, self, new_value):
                        log.warning('%s : Value "%s" for attribute %s of object %s is not unique.', self.unicity, new_value, self, obj)
                        return False
            return obj.entry.set_values(self.ldap_name, new_values, force_replace=force_replace or self.force_replace or self.write_only)
        return True

    def __repr__(self):
        """ Compute and return the “official” string representation of the attribute """
        return "<Attribute %s %s>" % (type(self).__name__, self.ldap_name)

    def __eq__(self, other):
        """ Check current attribute is equal to another """
        if not isinstance(other, self.__class__):
            return False
        return self.ldap_name == other.ldap_name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.ldap_name)

    def is_present(self, obj):
        """ Check if attribute is present/defined """
        return obj.entry.is_present(self.ldap_name)

    def is_unique(self):
        """ Check if attribute is unique """
        return isinstance(self.unicity, BaseUnicityCheck)

    def is_multiple(self):
        """ Check if attribute is multiple """
        return bool(self.multiple)

    def get_filter(self, value, match=None):
        """
        Get/compose LDAP filter on specific value for this attribute

        :param  value:  The python value of the attribute to search on.
                        Specific values:
                        - None : attribute not present
                        - '*' : attribute present
                        - list of string : list of alternative possible values. The filter will be
                        composed with OR logical operator.
        :param  match:  Match rule as accept by eesyldap.filters.compose (optional)
        """
        # If match rule is provided, compose filter with it via eesyldap.filters.compose
        if match is not None:
            ldap_value = self._to_ldap(value).decode('UTF8') if value is not None else value
            return compose_ldap_filter(self.ldap_name, match, ldap_value)
        # Filter on None value = attribute not present
        if value is None:
            return compose_ldap_filter(self.ldap_name, 'not_present')
        # Handle special '*' value = attribute present
        if value == '*':
            return compose_ldap_filter(self.ldap_name, 'present')
        # Handle multiple values = alternative values combine with OR logical operator
        if isinstance(value, list):
            if len(value) > 1:
                filterstrs = [self.get_filter(v) for v in value]
                return combine_ldap_filter('or', *filterstrs)
            return self.get_filter(value[0])

        # Convert value to LDAP
        ldap_value = self._to_ldap(value).decode('UTF8')

        # Detect and remove heading/trailing '*' to not escape it
        star_prefix = False
        star_suffix = False
        if ldap_value.startswith('*'):
            ldap_value = ldap_value[1:]
            star_prefix = True
        if ldap_value.endswith('*'):
            ldap_value = ldap_value[:-1]
            star_suffix = True

        # Define matching rule
        if star_prefix and star_suffix:
            match = 'contains'
        elif star_prefix:
            match = 'begins'
        elif star_suffix:
            match = 'ends'
        else:
            match = 'equals'

        return compose_ldap_filter(self.ldap_name, match, ldap_value)


class Text(Base):
    """
    LDAP text attribute

    On python side, the value of this attribute is manipulated as a built-in string object.
    """

    def _to_python(self, value, sortable=None):
        """ Convert attribute value from LDAP to Python """
        if sortable and value is None:
            return ''
        return value.decode('utf-8') if value is not None else None

    def _to_ldap(self, value):
        """ Convert attribute value from Python to LDAP """
        assert isinstance(value, str), "Text value must be a string (and not a %s)" % type(value)
        return value.encode('utf-8')


class Password(Text):
    """
    LDAP password attribute

    This type automatically handle to hash the password. It also expose some helper methods to
    manage LDAP hashed password values.

    On python side, the value of this attribute is manipulated as a built-in string object.
    """

    _hash_types = ['ssha', 'sha', 'md5', 'md5_crypt', 'ssha256', 'ssha512', 'clear']

    def __init__(self, name, hash_type=None, **kwargs):
        """
        Create a new LDAP attribute

        :param  name:               The attribute name
        :param  hash_type:          Password hash type. Default: SSHA
        """
        if hash_type is None:
            self.hash_type = 'ssha'
        else:
            assert hash_type in self._hash_types, 'Hash type incorrect. Must one of the following types : %s' % ', '.join(self._hash_types)
            self.hash_type = hash_type
        super().__init__(name, **kwargs)

    def verify(self, clear_password, hashed_passwords=None, obj=None):  # pylint: disable=too-many-return-statements
        """
        Verify the correspondence between an clear password and a hashed one

        :param  clear_password:     The clear password to check against hashed ones.
        :param  hashed_passwords:   The list of hashed passwords (Default: the attribute values if obj parameter is provided)
        :param  obj:                The LDAP object (optional and not used if hashed_passwords parameter is provided)
        """
        if hashed_passwords is None:
            assert isinstance(obj, LDAPObject), "If you don't specify hashed_passwords parameter, you must specify obj parameter"
            hashed_passwords = self.get_value(obj)
            if not hashed_passwords:
                log.debug('Password attribute %s : verify failed because the value of the attribute is empty', self.ldap_name)
                return False
            # log.debug('Password values retreived from object entry = %s', hashed_passwords)

        if not isinstance(hashed_passwords, list):
            hashed_passwords = [hashed_passwords]

        for hashed_password in hashed_passwords:
            hash_type = re.match('^{([^}]+)}', hashed_password)
            if not hash_type:
                # log.debug('Check clear password "%s" against another clear password "%s"', clear_password, hashed_password)
                return clear_password == hashed_password
            hash_type = hash_type.group(1)
            # log.debug('Check clear password "%s" against %s hashed password "%s"', clear_password, hash_type, hashed_password)
            if hash_type == 'MD5':
                if ldap_md5.verify(clear_password, hashed_password):
                    return True
                continue
            if hash_type == 'SHA':
                if ldap_sha1.verify(clear_password, hashed_password):
                    return True
                continue
            if hash_type == 'SSHA':
                if ldap_salted_sha1.verify(clear_password, hashed_password):
                    return True
                continue
            if hashed_password.startswith('{CRYPT}$1$'):
                if ldap_md5_crypt.verify(clear_password, hashed_password):
                    return True
                continue
            if hashed_password.startswith('{CRYPT}$5$'):
                if ldap_sha256_crypt.verify(clear_password, hashed_password):
                    return True
                continue
            if hashed_password.startswith('{CRYPT}$6$'):
                if ldap_sha512_crypt.verify(clear_password, hashed_password):
                    return True
                continue

            log.warning('Unrecognized hash password type (%s)', hash_type)

        return False

    @staticmethod
    def is_hashed_password(value):
        """ Check if the value is a hashed password """
        if not isinstance(value, str):
            return False
        if re.match('^({[^}]+})', value):
            return True
        return False

    def hash(self, password, hash_type=None):
        """
        Hash a password

        :param  password:       The password to hash
        :param  hash_type:      The hash type (optional, default: as configured in the constructor)
        """
        if hash_type is None:
            hash_type = self.hash_type

        log.debug("Hash password '%s' as %s", password, hash_type)

        if hash_type == 'clear':
            return password
        if hash_type == 'md5':
            return ldap_md5.hash(password)
        if hash_type == 'md5_crypt':
            return ldap_md5_crypt.hash(password)
        if hash_type == 'sha':
            return ldap_sha1.hash(password)
        if hash_type == 'ssha':
            return ldap_salted_sha1.hash(password)
        if hash_type == 'ssha256':
            return ldap_sha256_crypt.hash(password)
        if hash_type == 'ssha512':
            return ldap_sha512_crypt.hash(password)

        raise Exception('Unknwon hash type %s' % hash_type)

    def _to_ldap(self, value):
        """ Convert attribute value from Python to LDAP """
        return super()._to_ldap(value if self.is_hashed_password(value) else self.hash(value))


class Integer(Base):
    """
    LDAP integer attribute

    On python side, the value of this attribute is manipulated as a built-in integer object.
    """

    def _to_python(self, value, sortable=None):
        """ Convert attribute value from LDAP to Python """
        if sortable and value is None:
            return int()
        return int(value) if value is not None else None

    def _to_ldap(self, value):
        """ Convert attribute value from Python to LDAP """
        assert isinstance(value, int), "Integer value must be a integer (and not a %s)" % type(value)
        return str(value).encode('UTF8')


class Boolean(Base):
    """
    LDAP boolean attribute

    This type handle standard LDAP boolean attribute that stores the TRUE or FALSE values.

    On python side, the value of this attribute is manipulated as a built-in boolean object.
    """

    def _to_python(self, value, sortable=None):
        """ Convert attribute value from LDAP to Python """
        if sortable:
            # Return a sortable string value
            if value is None:
                return ''
            return 1 if value == b'TRUE' else 0
        return value == b'TRUE' if value is not None else None

    def _to_ldap(self, value):
        """ Convert attribute value from Python to LDAP """
        return b'TRUE' if value else b'FALSE'


class Datetime(Base):
    """
    LDAP datetime attribute

    This type handle standard LDAP Generalized Time attribute.

    On python side, the value of this attribute is manipulated as a datetime.datetime object.
    """

    def __init__(self, name, python_timezone=None, default_python_timezone=None, ldap_timezone=None, default_ldap_timezone=None, naive=None, **kwargs):
        """
        Create a new LDAP attribute

        :param  name:                       The attribute name
        :param  python_timezone:            Timezone use on python side (Default: local)
        :param  default_python_timezone:    Default timezone used if naive datetime is pass from python
                                            (Default: python_timezone)
        :param  ldap_timezone:              Timezone use on LDAP side (Default: UTC)
        :param  default_ldap_timezone:      Default timezone used if naive datetime is retreived from LDAP
                                            (not supposed to happen, default: ldap_timezone)
        :param  naive:                      Use naive datetime object : do not handle timezone on both Python
                                            and LDAP sides. Datetime are stored as UTC format on LDAP and Python
                                            datetime objects are naive.

        Timezone parameters possible values :
          - 'local' : Local server configured timezone
          - any value recognized by pytz.timezone()
        """
        self.python_timezone = self._convert_timezone_parameter('python_timezone', python_timezone, dateutil.tz.tzlocal())
        self.default_python_timezone = self._convert_timezone_parameter('default_python_timezone', default_python_timezone, self.python_timezone)
        self.ldap_timezone = self._convert_timezone_parameter('ldap_timezone', ldap_timezone, pytz.utc)
        self.default_ldap_timezone = self._convert_timezone_parameter('default_ldap_timezone', default_ldap_timezone, self.ldap_timezone)
        self.naive = naive
        super().__init__(name, **kwargs)

    @staticmethod
    def _convert_timezone_parameter(name, value, default):
        """ Convert constructor timezone parameter to timezone value """
        if value is None:
            return default
        if isinstance(value, str):
            if value == 'local':
                return dateutil.tz.tzlocal()
            return pytz.timezone(value)
        if isinstance(value, datetime.tzinfo):
            return value
        raise ValueError('Parameter %s must be a string or datetime.tzinfo object (not %s)' % (name, type(value)))

    def _to_python(self, value, sortable=None):
        """ Convert attribute value from LDAP to Python """
        if value is None:
            return '' if sortable else None
        date = dateutil.parser.parse(value, dayfirst=False)
        # Check if datetime
        if not date.tzinfo and not self.naive:
            if isinstance(self.default_ldap_timezone, pytz.tzinfo.DstTzInfo):
                date = self.default_ldap_timezone.localize(date)
            else:
                date = date.replace(tzinfo=self.default_ldap_timezone)
        elif self.naive:
            date = date.replace(tzinfo=None)
        if self.python_timezone and not self.naive:
            return date.astimezone(self.python_timezone)
        if sortable:
            if not self.naive:
                # Force UTC timezone (to make dates sortable together regardless their timezone)
                date = date.astimezone(pytz.utc)
            return date.strftime('%Y%m%d%H%M%S')
        return date

    def _to_ldap(self, value):
        """ Convert attribute value from Python to LDAP """
        assert isinstance(value, datetime.datetime), "Date value must be a datetime.datetime (and not a %s)" % type(value)
        if not value.tzinfo and not self.naive:
            if isinstance(self.default_python_timezone, pytz.tzinfo.DstTzInfo):
                from_value = self.default_python_timezone.localize(value)
            else:
                from_value = value.replace(tzinfo=self.default_python_timezone)
        elif self.naive:
            from_value = value.replace(tzinfo=None)
        else:
            from_value = copy.deepcopy(value)
        to_value = from_value.astimezone(self.ldap_timezone) if not self.naive else from_value
        datestring = to_value.strftime('%Y%m%d%H%M%S%z')
        if self.naive:
            datestring += 'Z'
        elif datestring.endswith('+0000'):
            datestring = datestring.replace('+0000', 'Z')
        return datestring.encode('utf-8')


class Date(Datetime):
    """
    LDAP date attribute

    This type handle standard LDAP Generalized Time attribute that store a date at midnight in UTC timezone.
    It derive from Datetime attribute type and support all of it parameters.

    On python side, the value of this attribute is manipulated as a datetime.date object.
    """

    def __init__(self, name, **kwargs):
        """
        Create a new LDAP attribute

        :param  name:                       The attribute name
        """
        kwargs['naive'] = True
        for kwarg in ['python_timezone', 'default_python_timezone', 'ldap_timezone', 'default_ldap_timezone']:
            assert kwarg not in kwargs, 'Date attribute is timezone naive on both LDAP and Python sides'
        super().__init__(name, **kwargs)

    def _to_python(self, value, sortable=None):
        """ Convert attribute value from LDAP to Python """
        if value is None:
            return '' if sortable else None
        if sortable:
            return super()._to_python(value, sortable=True)
        return super()._to_python(value).date()

    def _to_ldap(self, value):
        """ Convert attribute value from Python to LDAP """
        assert isinstance(value, datetime.date), "Date value must be a datetime.date (and not a %s)" % type(value)
        return super()._to_ldap(datetime.datetime.combine(value, datetime.datetime.min.time()))


class ShadowLastChange(Integer):
    """
    LDAP shadowLastChange attribute

    This type handle standard LDAP shadowLastChange attribute that store the date of the
    last password changed as an integer corresponding to number of days since 1970/01/01.

    On python side, the value of this attribute is manipulated as a datetime.date object.
    """

    def _to_python(self, value, sortable=None):
        value = super()._to_python(value)
        if value is None:
            return '' if sortable else None
        date = datetime.date(1970, 1, 1) + datetime.timedelta(days=value)
        if sortable:
            return date.strftime('%Y%m%d')
        return date

    def _to_ldap(self, value):
        assert isinstance(value, datetime.date), "Date value must be a datetime.date (and not a %s)" % type(value)
        return super()._to_ldap((value - datetime.date(1970, 1, 1)).days)


class JSON(Text):
    """
    LDAP JSON composited attribute

    On python side, the value of this attribute is manipulated as an object (or a list of objects
    if this attribute is multiple) as serialized in JSON.
    """

    def _to_python(self, value, sortable=None):
        if value is None and sortable:
            return ''
        value = super()._to_python(value, sortable=sortable)
        if value is None:
            return None
        return json.loads(value)

    def _to_ldap(self, value):
        value = json.dumps(value)
        return super()._to_ldap(value)
