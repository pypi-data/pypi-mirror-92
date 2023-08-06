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

""" Test on LDAP company object """

from eesyldap.search import LDAPSearch


def test_company_attributes_access(ee):
    """ Test access to company's attributes """
    assert ee.id == 'ee'
    assert ee.name == 'Easter-eggs'
    assert ee.mail == 'info@easter-eggs.com'
    assert ee.numid == 1
    assert ee.manager_dn == 'uid=brenard,ou=people,o=eesyldap'


def test_company_relations_access(ee, brenard, Group, Service):
    """ Test access to company relations """

    # Groups
    groups = ee.groups
    assert 'ldapsuperadmins' in groups
    assert isinstance(groups['ldapsuperadmins'], Group)
    assert groups['ldapsuperadmins'].dn == 'cn=ldapsuperadmins,ou=groups,o=eesyldap'

    # Manager
    assert ee.manager == brenard

    # Users
    users = ee.users
    assert isinstance(users, LDAPSearch) and users.filterstr == '(&(objectClass=top)(objectClass=inetOrgPerson)(objectClass=elPeople)(o=ee))'
    assert len(users) == 1
    assert brenard.username in users
    assert users[brenard.username] == brenard

    # Services
    services = ee.services
    assert isinstance(services, LDAPSearch) and services.filterstr == '(&(objectClass=top)(objectClass=organizationalUnit)(objectClass=elService)(o=ee))'
    assert len(services) == 2
    for service_id in services:
        assert service_id in ['admin', 'dev']
        assert isinstance(services[service_id], Service)
