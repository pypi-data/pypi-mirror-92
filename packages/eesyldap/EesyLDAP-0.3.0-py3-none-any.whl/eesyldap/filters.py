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

""" LDAP filter strings helpers """

import logging

from ldap.filter import escape_filter_chars

from eesyldap.exceptions import LDAPInvalidFilterLogicalOperator
from eesyldap.exceptions import LDAPInvalidFilterMatchRule

log = logging.getLogger(__name__)


def compose(attr_name, match, raw_value=None, escape=True, escape_mode=0):
    """
    Compose an LDAP filter string

    :param  attr_name:      The LDAP attribute name to filter on
    :param  match:          The match rule. Could be one of the following:
                            - "equals" or "=" or "=="
                            - "begins"
                            - "ends"
                            - "contains"
                            - "greater" or ">"
                            - "less" or "<"
                            - "greater_or_equal" or ">="
                            - "less_or_equal" or "<="
                            - "approx" or "~="
                            - "any" or "present"
    :param  raw_value:      The raw value of the LDAP attribute (optional, not need for "any" of "present" operators)
    :param  escape:         Escape or not the provided value (optional, default: True)
    :param  escape_mode:    Escape mode (if enabled):
                            - 0 (default) : only special chars mentioned in RFC 4515 are escaped
                            - 1 : all NON-ASCII chars are escaped
                            - 2 : all chars are escaped.
    """

    # Detect negation
    negate_filter = match.startswith('not_')
    if negate_filter:
        match = match[4:]

    assert raw_value is not None or match in ('present', 'any'), "The attribute value is not need only for 'present' or 'any' match rule"
    assert isinstance(escape_mode, int) and (escape_mode >= 0 or escape_mode <= 2)
    value = escape_filter_chars(raw_value, escape_mode=escape_mode) if raw_value is not None and escape else raw_value

    if match in ("equals", "=", "=="):
        filterstr = "({0}={1})".format(attr_name, value)
    elif match == "begins":
        filterstr = "({0}={1}*)".format(attr_name, value)
    elif match == "ends":
        filterstr = "({0}=*{1})".format(attr_name, value)
    elif match == "contains":
        filterstr = "({0}=*{1}*)".format(attr_name, value)
    elif match in ("greater", ">"):
        filterstr = "({0}>{1})".format(attr_name, value)
    elif match in ("less", "<"):
        filterstr = "({0}<{1})".format(attr_name, value)
    elif match in ("greater_or_equal", ">="):
        filterstr = "({0}>={1})".format(attr_name, value)
    elif match in ("less_or_equal", "<="):
        filterstr = "({0}<={1})".format(attr_name, value)
    elif match in ("approx", "~="):
        filterstr = "({0}~={1})".format(attr_name, value)
    elif match in ("any", "present"):
        filterstr = "({0}=*)".format(attr_name)
    else:
        raise LDAPInvalidFilterMatchRule(match)

    if negate_filter:
        return combine('not', filterstr)

    return filterstr


def combine(log_op, *filterstrs):
    """
    Combine LDAP filter strings

    :param  log_op:     The logical operator of the combination. Could be one of the following:
                        - "not" or "!"
                        - "and" or "&"
                        - "or" or '|'
    :param  filterstrs: The LDAP filter strings to combine
    """
    if log_op in ('not', '!'):
        assert len(filterstrs) == 1, "Only one filter string could be combined with NOT logical operator"
        return "(!%s)" % filterstrs[0]

    # Convert 'or' / 'and' logical operators
    log_op = '&' if log_op == 'and' else log_op
    log_op = '|' if log_op == 'or' else log_op
    if log_op in ('&', '|'):
        assert len(filterstrs) >= 2, "At least two filter strings could be combined with %s logical operator" % ('AND' if log_op == '&' else 'OR')
        return "(%s%s)" % (log_op, ''.join(filterstrs))

    raise LDAPInvalidFilterLogicalOperator(log_op)
