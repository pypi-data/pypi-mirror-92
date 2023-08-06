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

""" Test LDAP Password attribute type """

import pytest
from unittest.mock import patch

from eesyldap.attributes import Password
from eesyldap.object import LDAPObject

# pylint: disable=protected-access,redefined-outer-name


def test_create_all_hash_types():
    """ Test to create LDAP Password attribute with each supported hash types """
    for hash_type in Password._hash_types:
        Password('fakeAttr', hash_type=hash_type)


def test_create_without_hash_types():
    """ Test to create LDAP Password attribute without specify hash type """
    Password('fakeAttr')


def test_create_bad_hash_type():
    """ Test to create LDAP Password attribute with bad hash type """
    with pytest.raises(AssertionError):
        Password('fakeAttr', hash_type='fake')


def test_hash_and_verify_md5():
    """ Test to hash and verify a MD5 password """
    attr = Password('fakeAttr', hash_type='md5')
    clear_password = 'azerty'
    hashed_password = attr.hash(clear_password)

    assert hashed_password == '{MD5}q09j+axlFSV1iGhg3eSAoQ=='

    assert attr.verify(clear_password, hashed_passwords=[hashed_password])


def test_hash_and_verify_md5_crypt():
    """ Test to hash and verify a MD5 CRIPT password """
    attr = Password('fakeAttr', hash_type='md5_crypt')
    clear_password = 'azerty'
    hashed_password = attr.hash(clear_password)

    assert isinstance(hashed_password, str) and hashed_password.startswith('{CRYPT}$1$')
    assert len(hashed_password) == 41

    assert attr.verify(clear_password, hashed_passwords=[hashed_password])


def test_hash_and_verify_sha():
    """ Test to hash and verify a SHA password """
    attr = Password('fakeAttr', hash_type='sha')
    clear_password = 'azerty'
    hashed_password = attr.hash(clear_password)

    assert hashed_password == '{SHA}nPldrNIm3PQ9o3bNtsu6cDUhiSE='

    assert attr.verify(clear_password, hashed_passwords=[hashed_password])


def test_hash_and_verify_ssha():
    """ Test to hash and verify a SSHA password """
    attr = Password('fakeAttr', hash_type='ssha')
    clear_password = 'azerty'
    hashed_password = attr.hash(clear_password)

    assert isinstance(hashed_password, str) and hashed_password.startswith('{SSHA}')
    assert len(hashed_password) == 38

    assert attr.verify(clear_password, hashed_passwords=[hashed_password])


def test_hash_and_verify_ssha256():
    """ Test to hash and verify a SSHA256 password """
    attr = Password('fakeAttr', hash_type='ssha256')
    clear_password = 'azerty'
    hashed_password = attr.hash(clear_password)

    assert isinstance(hashed_password, str) and hashed_password.startswith('{CRYPT}$5$')
    assert len(hashed_password) == 84

    assert attr.verify(clear_password, hashed_passwords=[hashed_password])


def test_hash_and_verify_ssha512():
    """ Test to hash and verify a SSHA512 password """
    attr = Password('fakeAttr', hash_type='ssha512')
    clear_password = 'azerty'
    hashed_password = attr.hash(clear_password)

    assert isinstance(hashed_password, str) and hashed_password.startswith('{CRYPT}$6$')
    assert len(hashed_password) == 127

    assert attr.verify(clear_password, hashed_passwords=[hashed_password])


def test_hash_and_verify_clear():
    """ Test to hash and verify a clear password """
    attr = Password('fakeAttr', hash_type='clear')
    clear_password = 'azerty'
    hashed_password = attr.hash(clear_password)

    assert hashed_password == clear_password

    assert attr.verify(clear_password, hashed_passwords=[hashed_password])


def test_verify_clear_password():
    """ Test to verify a clear password """
    attr = Password('fakeAttr', hash_type='ssha256')
    assert attr.verify('clear', hashed_passwords=['clear'])
    assert not attr.verify('clear', hashed_passwords=['not_clear'])


def test_verify_without_hashed_passwords(brenard):
    """
    Test to verify password without specify hashed_passwords but providing LDAP object """
    assert brenard._attrs['password'].verify('password', obj=brenard)


def test_is_hashed_password_when_true():
    """ Test the is_hashed_password method when it is True """
    assert Password.is_hashed_password('{SHA}nPldrNIm3PQ9o3bNtsu6cDUhiSE=')


def test_is_hashed_password_when_false():
    """ Test the is_hashed_password method when it is not True """
    assert not Password.is_hashed_password('clear')


def test_to_ldap_clear_password():
    """ Test LDAP Password attribute _to_ldap method with a clear password """
    attr = Password('fakeAttr', hash_type='sha')
    assert attr._to_ldap('ascii') == b'{SHA}UcBms26osyB2lkx2b4oDJMpOtLk='


def test_to_ldap_hashed_password():
    """ Test LDAP Password attribute _to_ldap method with a hashed password """
    attr = Password('fakeAttr', hash_type='sha')
    assert attr._to_ldap('{SHA}qUqP5cyxm6YcTAhz05Hph5gvu9M=') == b'{SHA}qUqP5cyxm6YcTAhz05Hph5gvu9M='
