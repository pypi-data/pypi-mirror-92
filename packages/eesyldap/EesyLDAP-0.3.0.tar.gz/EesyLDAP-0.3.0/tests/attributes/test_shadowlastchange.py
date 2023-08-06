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

""" Test LDAP ShadowLastChange attribute type """

from datetime import date
import pytest

from eesyldap.attributes import ShadowLastChange

# pylint: disable=protected-access,redefined-outer-name


@pytest.fixture
def fake_attr():
    """ Generate a fake LDAP ShadowLastChange attribute """
    return ShadowLastChange('fakeAttr')


def test_to_python(fake_attr):
    """ Test LDAP ShadowLastChange attribute _to_python method """
    assert fake_attr._to_python(b'1') == date(1970, 1, 2)
    assert fake_attr._to_python(b'0') == date(1970, 1, 1)
    assert fake_attr._to_python(b'18277') == date(2020, 1, 16)
    assert fake_attr._to_python(None) is None


def test_to_python_sortable(fake_attr):
    """ Test LDAP ShadowLastChange attribute _to_python method with sortable=True """
    assert fake_attr._to_python(b'1', sortable=True) == '19700102'
    assert fake_attr._to_python(b'0', sortable=True) == '19700101'
    assert fake_attr._to_python(None, sortable=True) == ''


def test_to_ldap(fake_attr):
    """ Test LDAP ShadowLastChange attribute _to_ldap method """
    assert fake_attr._to_ldap(date(1970, 1, 2)) == b'1'
    assert fake_attr._to_ldap(date(2020, 1, 16)) == b'18277'
    with pytest.raises(AssertionError):
        fake_attr._to_ldap(None)
