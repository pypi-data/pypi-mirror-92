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

""" Test on LDAP service object """

import pytest

from eesyldap.exceptions import LDAPRelatedObjectModifed
from eesyldap.exceptions import LDAPRequiredAttribute
from eesyldap.search import LDAPSearch


def test_service_attributes_access(dev):
    """ Test access to service's attributes """
    assert dev.id == 'dev'
    assert dev.name == 'Dev'
    assert dev.mail == 'dev@easter-eggs.com'
    assert dev.numid == 3
    assert dev.manager_dn == 'uid=brenard,ou=people,o=eesyldap'


def test_service_relations_access(dev, brenard, ee, Group):     # pylint: disable=unused-argument
    """
    Test access to company relations

    Note : Group parameter is need to be sure Group object type is declared.
    """

    # Groups
    groups = dev.groups
    assert isinstance(groups, LDAPSearch) and groups.filterstr == '(&(objectClass=top)(objectClass=elGroup)(ou=dev))'
    assert not groups

    # Manager
    assert dev.manager == brenard

    # Users
    users = dev.users
    assert isinstance(users, LDAPSearch) and users.filterstr == '(&(objectClass=top)(objectClass=inetOrgPerson)(objectClass=elPeople)(ou=dev))'
    assert len(users) == 1
    assert brenard.username in users
    assert users[brenard.username] == brenard

    # Company
    assert dev.company == ee


def test_service_remove_company(dev):
    """ Test to remove service's company """
    with pytest.raises(LDAPRequiredAttribute):
        dev.company = None


def test_service_add_user(dev, brenard):
    """ Test to add a user to service """
    users = dict(dev.users)
    users[brenard.username] = brenard
    dev.users = users

    # Verify
    brenard.refresh()
    assert 'dev' in brenard.service_ids


def test_service_remove_user(admin, brenard):
    """ Test to remove a user to service """
    users = dict(admin.users)
    del users[brenard.username]
    admin.users = users

    # Verify
    brenard.refresh()
    assert 'admin' not in brenard.service_ids


def test_service_add_modified_user(dev, jdoe):
    """ Test to add a modified user to service """
    jdoe.numid = 88
    users = dict(dev.users)
    users[jdoe.username] = jdoe

    with pytest.raises(LDAPRelatedObjectModifed):
        dev.users = users


def test_service_set_manager(dev, jdoe):
    """ Test to set manager of a service """
    dev.manager = jdoe
    dev.refresh()

    assert dev.manager_dn == jdoe.dn


def test_service_set_modified_manager(dev, brenard):
    """ Test to set a modified user as manager of a service """
    brenard.numid = 77
    with pytest.raises(LDAPRelatedObjectModifed):
        dev.manager = brenard


def test_service_remove_company_using_reverse_relation(dev, ee):
    """ Test to remove a service's company using the reverse relation """
    services = dict(ee.services)
    del services[dev.id]
    with pytest.raises(LDAPRequiredAttribute):
        ee.services = services
