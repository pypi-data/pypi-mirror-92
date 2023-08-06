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

""" Exceptions raised during test """

from eesyldap.exceptions import LDAPInvalidAttributeValue


class CantReuseSamePassword(LDAPInvalidAttributeValue):
    """ Raised when the same password as current one is affected to a user """

    def __init__(self, attr_name, attr_value):
        super().__init__(attr_name, attr_value, msg="You can't reuse the same password")


class CantReuseOldPassword(LDAPInvalidAttributeValue):
    """ Raised when the previously used password is affected to a user """

    def __init__(self, attr_name, attr_value):
        super().__init__(attr_name, attr_value, msg="You can't reuse an old password")
