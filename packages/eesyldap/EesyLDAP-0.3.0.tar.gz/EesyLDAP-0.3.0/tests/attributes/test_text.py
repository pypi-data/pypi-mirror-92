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

""" Test LDAP Text attribute type """

import pytest

from eesyldap.attributes import Text

# pylint: disable=protected-access,redefined-outer-name


@pytest.fixture
def fake_attr():
    """ Generate a fake LDAP Text attribute """
    return Text('fakeAttr')


def test_to_python(fake_attr):
    """ Test LDAP Text attribute _to_python method """
    assert fake_attr._to_python(b'ascii') == 'ascii'
    assert fake_attr._to_python('ÀbĈ'.encode('utf8')) == u'ÀbĈ'
    assert fake_attr._to_python(None) is None


def test_to_python_sortable(fake_attr):
    """ Test LDAP Text attribute _to_python method with sortable=True """
    assert fake_attr._to_python(None, sortable=True) == ''
    assert fake_attr._to_python('ascii'.encode('utf8'), sortable=True) == 'ascii'


def test_to_ldap(fake_attr):
    """ Test LDAP Text attribute _to_ldap method """
    assert fake_attr._to_ldap('ascii') == b'ascii'
    assert fake_attr._to_ldap('ÀbĈ') == 'ÀbĈ'.encode('utf8')
    with pytest.raises(AssertionError):
        fake_attr._to_ldap(None)
