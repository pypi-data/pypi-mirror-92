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

""" Test LDAP Datetime attribute type """

from datetime import datetime
import pytest
import pytz

from eesyldap.attributes import Datetime

# pylint: disable=protected-access,redefined-outer-name


@pytest.fixture
def tz_paris():
    """ Retreive Europe/Paris timezone object """
    return pytz.timezone('Europe/Paris')


def test_create_with_timezone_local():
    """ Test to create LDAP Datetime attribute with timezone local """
    Datetime('fakeAttr', python_timezone='local', ldap_timezone='local')


def test_create_with_timezone_europe_paris():
    """ Test to create LDAP Datetime attribute with timezone Europe/Paris """
    Datetime('fakeAttr', python_timezone='Europe/Paris', ldap_timezone='Europe/Paris')


def test_create_with_timezone_object(tz_paris):
    """ Test to create LDAP Datetime attribute with a timezone object """
    Datetime('fakeAttr', python_timezone=tz_paris, ldap_timezone=pytz.utc)


def test_create_with_naive_timezone():
    """ Test to create LDAP Datetime attribute with naive timezone """
    Datetime('fakeAttr', naive=True)


@pytest.fixture
def fake_attr_naive():
    """ Generate a fake LDAP Date attribute with naive timezone """
    return Datetime('fakeAttr', naive=True)


def test_to_python_naive(fake_attr_naive):
    """ Test LDAP Datetime attribute _to_python method with naive timezone"""
    assert fake_attr_naive._to_python(b'19971010000000Z') == datetime(1997, 10, 10, 0, 0, 0)
    assert fake_attr_naive._to_python(b'20200116121212Z') == datetime(2020, 1, 16, 12, 12, 12)
    assert fake_attr_naive._to_python(b'20200116121212+0100') == datetime(2020, 1, 16, 12, 12, 12)
    assert fake_attr_naive._to_python(None) is None


def test_to_python_sortable_naive(fake_attr_naive):
    """ Test LDAP Datetime attribute _to_python method with sortable=True and naive timezone """
    assert fake_attr_naive._to_python(b'19971010000000Z', sortable=True) == '19971010000000'
    assert fake_attr_naive._to_python(b'20200116121212Z', sortable=True) == '20200116121212'
    assert fake_attr_naive._to_python(b'20200116121212+0100', sortable=True) == '20200116121212'
    assert fake_attr_naive._to_python(None, sortable=True) == ''


def test_to_ldap_naive(fake_attr_naive):
    """ Test LDAP Datetime attribute _to_ldap method with naive timezone """
    assert fake_attr_naive._to_ldap(datetime(1997, 11, 21, 15, 12, 54)) == b'19971121151254Z'
    assert fake_attr_naive._to_ldap(datetime(2020, 1, 17, 00, 23, 55)) == b'20200117002355Z'
    with pytest.raises(AssertionError):
        fake_attr_naive._to_ldap(None)


@pytest.fixture
def fake_attr_utc_paris(tz_paris):
    """
    Generate a fake LDAP Date attribute with UTC timezone in LDAP
    and Europe/Paris timezone on Python side.
    """
    return Datetime('fakeAttr', ldap_timezone=pytz.utc, python_timezone=tz_paris)


def test_to_python_utc_paris(fake_attr_utc_paris, tz_paris):
    """ Test LDAP Datetime attribute _to_python method with naive timezone"""
    assert fake_attr_utc_paris._to_python(b'19971010000000Z') == datetime(1997, 10, 10, 0, 0, 0, tzinfo=pytz.utc).astimezone(tz_paris)
    assert fake_attr_utc_paris._to_python(b'20200116121212Z') == datetime(2020, 1, 16, 12, 12, 12, tzinfo=pytz.utc).astimezone(tz_paris)
    assert fake_attr_utc_paris._to_python(b'20200116121212+0100') == datetime(2020, 1, 16, 11, 12, 12, tzinfo=pytz.utc).astimezone(tz_paris)
    assert fake_attr_utc_paris._to_python(None) is None


def test_to_ldap_utc_paris(fake_attr_utc_paris, tz_paris):
    """ Test LDAP Datetime attribute _to_python method with naive timezone"""
    assert fake_attr_utc_paris._to_ldap(datetime(1997, 11, 21, 15, 12, 54, tzinfo=pytz.utc).astimezone(tz_paris)) == b'19971121151254Z'
    assert fake_attr_utc_paris._to_ldap(datetime(2020, 1, 17, 00, 23, 55, tzinfo=pytz.utc).astimezone(tz_paris)) == b'20200117002355Z'
    with pytest.raises(AssertionError):
        fake_attr_utc_paris._to_ldap(None)


@pytest.fixture
def fake_attr_paris_paris(tz_paris):
    """
    Generate a fake LDAP Date attribute with Europe/Paris timezone in both
    LDAP and Python sides.
    """
    return Datetime('fakeAttr', ldap_timezone=tz_paris, python_timezone=tz_paris)


def test_to_python_paris_paris(fake_attr_paris_paris, tz_paris):
    """ Test LDAP Datetime attribute _to_python method with naive timezone"""
    assert fake_attr_paris_paris._to_python(b'19971010000000+0200') == datetime(1997, 10, 9, 22, 0, 0, tzinfo=pytz.utc).astimezone(tz_paris)
    assert fake_attr_paris_paris._to_python(b'20200716121212+0100') == datetime(2020, 7, 16, 11, 12, 12, tzinfo=pytz.utc).astimezone(tz_paris)
    assert fake_attr_paris_paris._to_python(b'20200116121212Z') == datetime(2020, 1, 16, 12, 12, 12, tzinfo=pytz.utc).astimezone(tz_paris)
    assert fake_attr_paris_paris._to_python(None) is None


def test_to_ldap_paris_paris(fake_attr_paris_paris, tz_paris):
    """ Test LDAP Datetime attribute _to_python method with naive timezone"""
    assert fake_attr_paris_paris._to_ldap(datetime(1997, 11, 21, 15, 12, 54, tzinfo=pytz.utc).astimezone(tz_paris)) == b'19971121161254+0100'
    assert fake_attr_paris_paris._to_ldap(datetime(2020, 7, 17, 00, 23, 55, tzinfo=pytz.utc).astimezone(tz_paris)) == b'20200717022355+0200'
    with pytest.raises(AssertionError):
        fake_attr_paris_paris._to_ldap(None)
