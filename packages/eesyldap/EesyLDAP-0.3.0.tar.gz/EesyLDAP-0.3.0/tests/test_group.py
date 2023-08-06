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

""" Test on LDAP group object """


def test_group_attributes_access(ldapsuperadmins):
    """ Test access to group's attributes """
    assert ldapsuperadmins.name == 'ldapsuperadmins'
    assert ldapsuperadmins.description == 'Super admins of the LDAP directory'
    assert ldapsuperadmins.company_id == 'ee'
    assert ldapsuperadmins.member_usernames == ['brenard']
    assert ldapsuperadmins.member_dns == ['uid=brenard,ou=people,o=eesyldap']
    assert ldapsuperadmins.owner_dn == 'uid=brenard,ou=people,o=eesyldap'


def test_group_relations_access(ldapsuperadmins, brenard, ee):
    """ Test access to group relations """

    # Members
    members = ldapsuperadmins.members
    assert len(members) == 1
    assert brenard.username in members
    assert members[brenard.username] == brenard

    # Owner
    assert ldapsuperadmins.owner == brenard

    # User owned group
    assert ldapsuperadmins.name in brenard.owned_groups

    # Company
    assert ldapsuperadmins.company == ee

    # Services
    services = ldapsuperadmins.services
    assert isinstance(services, dict)
    assert not services


def test_group_add_member(ldapsuperadmins, jdoe):
    """ Test to add a user to group as member """
    members = ldapsuperadmins.members.copy()
    members[jdoe.dn] = jdoe
    ldapsuperadmins.members = members

    assert jdoe.username in ldapsuperadmins.member_usernames
    assert jdoe.dn in ldapsuperadmins.member_dns


def test_group_remove_member(ldapsuperadmins, brenard):
    """ Test to remove a group's member """
    members = ldapsuperadmins.members.copy()
    del members[brenard.username]
    ldapsuperadmins.members = members

    assert brenard.username not in ldapsuperadmins.member_usernames
    assert brenard.dn not in ldapsuperadmins.member_dns


def test_group_remove_all_members(ldapsuperadmins):
    """ Test to remove all group's members """
    ldapsuperadmins.members = dict()

    assert not ldapsuperadmins.member_usernames
    assert not ldapsuperadmins.member_dns


def test_group_delete_member(ldapsuperadmins, jdoe):
    """ Test to delete a group's member """
    members = ldapsuperadmins.members.copy()
    members[jdoe.dn] = jdoe
    ldapsuperadmins.members = members

    jdoe.delete()
    ldapsuperadmins.refresh()

    assert jdoe.username not in ldapsuperadmins.member_usernames
    assert jdoe.dn not in ldapsuperadmins.member_dns
