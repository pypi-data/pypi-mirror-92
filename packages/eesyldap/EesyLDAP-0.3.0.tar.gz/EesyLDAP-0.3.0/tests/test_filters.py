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

""" Tests on LDAP filters helpers """

import pytest

from eesyldap.exceptions import LDAPInvalidFilterLogicalOperator
from eesyldap.exceptions import LDAPInvalidFilterMatchRule
from eesyldap.filters import combine
from eesyldap.filters import compose


def test_compose_equals():
    assert compose('fakeAttr', 'equals', 'value') == '(fakeAttr=value)'
    assert compose('fakeAttr', '=', 'value') == '(fakeAttr=value)'
    assert compose('fakeAttr', '==', 'value') == '(fakeAttr=value)'


def test_compose_not_equals():
    assert compose('fakeAttr', 'not_equals', 'value') == '(!(fakeAttr=value))'


def test_compose_equals_none():
    with pytest.raises(AssertionError):
        compose('fakeAttr', 'equals')


def test_compose_begins():
    assert compose('fakeAttr', 'begins', 'value') == '(fakeAttr=value*)'


def test_compose_not_begins():
    assert compose('fakeAttr', 'not_begins', 'value') == '(!(fakeAttr=value*))'


def test_compose_ends():
    assert compose('fakeAttr', 'ends', 'value') == '(fakeAttr=*value)'


def test_compose_not_ends():
    assert compose('fakeAttr', 'not_ends', 'value') == '(!(fakeAttr=*value))'


def test_compose_contains():
    assert compose('fakeAttr', 'contains', 'value') == '(fakeAttr=*value*)'


def test_compose_not_contains():
    assert compose('fakeAttr', 'not_contains', 'value') == '(!(fakeAttr=*value*))'


def test_compose_greater():
    assert compose('fakeAttr', 'greater', '1') == '(fakeAttr>1)'
    assert compose('fakeAttr', '>', '1') == '(fakeAttr>1)'


def test_compose_not_greater():
    assert compose('fakeAttr', 'not_greater', '1') == '(!(fakeAttr>1))'


def test_compose_less():
    assert compose('fakeAttr', 'less', '1') == '(fakeAttr<1)'
    assert compose('fakeAttr', '<', '1') == '(fakeAttr<1)'


def test_compose_not_less():
    assert compose('fakeAttr', 'not_less', '1') == '(!(fakeAttr<1))'


def test_compose_greater_or_equal():
    assert compose('fakeAttr', 'greater_or_equal', '1') == '(fakeAttr>=1)'
    assert compose('fakeAttr', '>=', '1') == '(fakeAttr>=1)'


def test_compose_not_greater_or_equal():
    assert compose('fakeAttr', 'not_greater_or_equal', '1') == '(!(fakeAttr>=1))'


def test_compose_less_or_equal():
    assert compose('fakeAttr', 'less_or_equal', '1') == '(fakeAttr<=1)'
    assert compose('fakeAttr', '<=', '1') == '(fakeAttr<=1)'


def test_compose_not_less_or_equal():
    assert compose('fakeAttr', 'not_less_or_equal', '1') == '(!(fakeAttr<=1))'


def test_compose_approx():
    assert compose('fakeAttr', 'approx', 'value') == '(fakeAttr~=value)'
    assert compose('fakeAttr', '~=', 'value') == '(fakeAttr~=value)'


def test_compose_not_approx():
    assert compose('fakeAttr', 'not_approx', 'value') == '(!(fakeAttr~=value))'


def test_compose_present():
    assert compose('fakeAttr', 'present') == '(fakeAttr=*)'
    assert compose('fakeAttr', 'any') == '(fakeAttr=*)'


def test_compose_not_present():
    assert compose('fakeAttr', 'not_present') == '(!(fakeAttr=*))'
    assert compose('fakeAttr', 'not_any') == '(!(fakeAttr=*))'


def test_compose_invalid_match():
    with pytest.raises(LDAPInvalidFilterMatchRule):
        assert compose('fakeAttr', 'error', 'value')


def test_compose_dont_escape_value():
    values = '*()\\\u0000ée'
    for char in values:
        assert compose('fakeAttr', '==', char, escape=False) == '(fakeAttr=%s)' % char


def test_compose_escape_values():
    values = [
        ('*', '\\2a'),
        ('(', '\\28'),
        (')', '\\29'),
        ('\\', '\\5c'),
        ('\u0000', '\\00'),
        ('é', 'é'),
        ('e', 'e')
    ]
    for value, escape_value in values:
        assert compose('fakeAttr', '==', value, escape_mode=0) == '(fakeAttr=%s)' % escape_value


def test_compose_escape_values_nonascii_chars():
    values = [
        ('*', '\\2a'),
        ('(', '\\28'),
        (')', '\\29'),
        ('\\', '\\5c'),
        ('\u0000', '\\00'),
        ('é', '\\e9'),
        ('e', 'e')
    ]
    for value, escape_value in values:
        assert compose('fakeAttr', '==', value, escape_mode=1) == '(fakeAttr=%s)' % escape_value


def test_compose_escape_values_all_chars():
    values = [
        ('*', '\\2a'),
        ('(', '\\28'),
        (')', '\\29'),
        ('\\', '\\5c'),
        ('\u0000', '\\00'),
        ('é', '\\e9'),
        ('e', '\\65')
    ]
    for value, escape_value in values:
        assert compose('fakeAttr', '==', value, escape_mode=2) == '(fakeAttr=%s)' % escape_value


def test_combine_and():
    assert combine('and', '(fakeAttr1=test1)', '(fakeAttr2=test2)') == '(&(fakeAttr1=test1)(fakeAttr2=test2))'
    assert combine('&', '(fakeAttr1=test1)', '(fakeAttr2=test2)') == '(&(fakeAttr1=test1)(fakeAttr2=test2))'
    with pytest.raises(AssertionError):
        combine('and', '(fakeAttr1=test1)')
    with pytest.raises(AssertionError):
        combine('&', '(fakeAttr1=test1)')


def test_combine_or():
    assert combine('or', '(fakeAttr1=test1)', '(fakeAttr2=test2)') == '(|(fakeAttr1=test1)(fakeAttr2=test2))'
    assert combine('|', '(fakeAttr1=test1)', '(fakeAttr2=test2)') == '(|(fakeAttr1=test1)(fakeAttr2=test2))'
    with pytest.raises(AssertionError):
        combine('or', '(fakeAttr1=test1)')
    with pytest.raises(AssertionError):
        combine('|', '(fakeAttr1=test1)')


def test_combine_not():
    assert combine('not', '(fakeAttr1=test1)') == '(!(fakeAttr1=test1))'
    assert combine('!', '(fakeAttr1=test1)') == '(!(fakeAttr1=test1))'
    with pytest.raises(AssertionError):
        combine('not', '(fakeAttr1=test1)', '(fakeAttr2=test2)')
    with pytest.raises(AssertionError):
        combine('!', '(fakeAttr1=test1)', '(fakeAttr2=test2)')


def test_combine_invalid_log_op():
    with pytest.raises(LDAPInvalidFilterLogicalOperator):
        assert combine('error', '(fakeAttr1=test1)', '(fakeAttr2=test2)')
