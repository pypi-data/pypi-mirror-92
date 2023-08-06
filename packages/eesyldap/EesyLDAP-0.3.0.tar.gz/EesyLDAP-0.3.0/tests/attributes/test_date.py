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

""" Test LDAP Date attribute type """

from datetime import date
import pytest

from eesyldap.attributes import Date

# pylint: disable=protected-access,redefined-outer-name


def test_create_with_timezone():
    """ Test to create LDAP Date attribute with timezone parameters """
    with pytest.raises(AssertionError):
        Date('fakeAttr', python_timezone='local')
    with pytest.raises(AssertionError):
        Date('fakeAttr', default_python_timezone='local')
    with pytest.raises(AssertionError):
        Date('fakeAttr', ldap_timezone='local')
    with pytest.raises(AssertionError):
        Date('fakeAttr', default_ldap_timezone='local')


@pytest.fixture
def fake_attr():
    """ Generate a fake LDAP Date attribute """
    return Date('fakeAttr')


def test_to_python(fake_attr):
    """ Test LDAP Date attribute _to_python method """
    assert fake_attr._to_python(b'19971010000000Z') == date(1997, 10, 10)
    assert fake_attr._to_python(b'20200116121212Z') == date(2020, 1, 16)
    assert fake_attr._to_python(b'20200116121212+0001') == date(2020, 1, 16)
    assert fake_attr._to_python(None) is None


def test_to_python_sortable(fake_attr):
    """ Test LDAP Date attribute _to_python method with sortable=True """
    assert fake_attr._to_python(b'19971010000000Z', sortable=True) == '19971010000000'
    assert fake_attr._to_python(b'20200116121212Z', sortable=True) == '20200116121212'
    assert fake_attr._to_python(b'20200116121212+0001', sortable=True) == '20200116121212'
    assert fake_attr._to_python(None, sortable=True) == ''


def test_to_ldap(fake_attr):
    """ Test LDAP Date attribute _to_ldap method """
    assert fake_attr._to_ldap(date(1997, 11, 21)) == b'19971121000000Z'
    assert fake_attr._to_ldap(date(2020, 1, 16)) == b'20200116000000Z'
    with pytest.raises(AssertionError):
        fake_attr._to_ldap(None)
