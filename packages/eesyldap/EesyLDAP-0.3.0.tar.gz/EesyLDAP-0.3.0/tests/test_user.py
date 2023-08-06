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

""" Test on LDAP User object """

import datetime
import pytest

from eesyldap.exceptions import LDAPAttributeUnicityError
from eesyldap.exceptions import LDAPNotUniqueAttribute
from eesyldap.exceptions import LDAPRequiredAttribute
from eesyldap.exceptions import LDAPSearchHardLimitExceeded
from eesyldap.exceptions import LDAPSearchLimitExceeded
from eesyldap.search import LDAPSearch

from tests.exceptions import CantReuseOldPassword
from tests.exceptions import CantReuseSamePassword


def test_user_attributes_access(brenard):
    """ Check attributes values access """
    assert brenard.username == 'brenard'
    assert brenard.firstname == 'Benjamin'
    assert brenard.lastname == 'Renard'
    assert brenard.fullname == 'Benjamin Renard'
    assert brenard.fullname_normalized == 'Benjamin Renard'
    assert brenard.mail == 'brenard@easter-eggs.com'
    assert brenard.company_id == 'ee'
    assert sorted(brenard.service_ids) == ['admin', 'dev']
    assert isinstance(brenard.enabled, bool) and brenard.enabled
    assert isinstance(brenard.start_date, datetime.date) and brenard.start_date == datetime.date(year=2006, month=10, day=10)
    assert brenard.end_date is None
    assert isinstance(brenard.birth_date, datetime.date) and brenard.birth_date == datetime.date(year=1986, month=12, day=18)
    assert brenard.numid == 4
    assert brenard.bank_details == [dict(
        iban="FR76 3000 3034 3900 0504 9292 376",
        bic="SOGEFRPP",
        label="defaut"
    )]


def test_user_relations_access(brenard, Company, Service, Group):
    """ Test access to brenard relations """

    # Company
    company = brenard.company
    assert isinstance(company, Company) and company.dn == 'o=ee,ou=companies,o=eesyldap'

    # Managed company
    managed_company = brenard.managed_company
    assert isinstance(managed_company, Company)
    assert managed_company.dn == 'o=ee,ou=companies,o=eesyldap'
    assert managed_company.manager == brenard

    # Services
    services = brenard.services
    assert isinstance(services, dict)
    # Search is implicitly runned using len()
    assert len(services) == len(brenard.service_ids)
    for service_id, service in services.items():
        assert isinstance(service, Service)
        assert service.id == service_id
        assert service_id in brenard.service_ids
        assert service.manager == brenard

    # Managed services
    managed_services = brenard.managed_services
    assert isinstance(managed_services, LDAPSearch)
    assert managed_services.filterstr == "(&(objectClass=top)(objectClass=organizationalUnit)(objectClass=elService)(manager=uid=brenard,ou=people,o=eesyldap))"

    managed_services = dict(managed_services)
    assert len(managed_services) == 2
    for service_id, service in managed_services.items():
        assert isinstance(service, Service) and service_id in ['admin', 'dev']
        assert service.manager_dn == brenard.dn
        assert service.manager == brenard

    # Groups
    groups = brenard.groups
    assert isinstance(groups, LDAPSearch)
    # Search is implicitly runned using items()
    for group_name, group in groups.items():
        assert isinstance(group, Group)
        assert group.name == group_name
        assert brenard.dn in group.member_dns
        assert brenard.username in group.members
        assert brenard.username in group.members_by_username

    # Owned groups
    owned_groups = brenard.owned_groups
    assert isinstance(owned_groups, LDAPSearch) and owned_groups.filterstr == "(&(objectClass=top)(objectClass=elGroup)(owner=uid=brenard,ou=people,o=eesyldap))"
    assert len(owned_groups) == 1
    for group_name, group in owned_groups.items():
        assert isinstance(group, Group)
        assert group.name == group_name
        assert group.owner_dn == brenard.dn
        assert group.owner == brenard


def test_user_object_attribute_wrapper(brenard):
    """ Test object attributes wrapper """
    assert brenard.username == brenard.attrs.username.get_value()
    assert brenard.attrs.username.is_unique()


def test_user_save(brenard):
    """ Test changing user name """
    brenard.lastname = 'Fox'
    brenard.save()
    assert brenard.lastname == 'Fox'
    assert brenard.fullname == 'Benjamin Fox'


def test_user_update(brenard):
    """ Test multiple changes on user """
    changes = dict(
        username='b.renard',
        birth_date=datetime.date(1978, 12, 18),
        enabled=False,
    )
    brenard.update(changes)
    assert brenard.username == 'b.renard'
    assert brenard.birth_date == changes['birth_date']
    assert brenard.enabled == changes['enabled']


def test_user_password_change(brenard):
    """ Test change user password """
    new_password = "azerty"
    brenard.password = new_password
    brenard.save()

    assert brenard.password_last_change == datetime.date.today()
    assert brenard.attrs.password.verify(new_password)


def test_user_password_reuse_same(brenard):
    """ Test reuse same password is forbidden """
    new_password = "qwerty"
    brenard.password = new_password
    brenard.save()

    with pytest.raises(CantReuseSamePassword):
        brenard.password = new_password


def test_user_password_reuse_old(brenard):
    """ Test reuse an old password is forbidden """
    old_password = "azerty"
    new_password = "qwerty"
    brenard.password = old_password
    brenard.save()

    brenard.password = new_password
    brenard.save()

    with pytest.raises(CantReuseOldPassword):
        brenard.password = old_password


def test_user_unset_set_relation(brenard, ldap_client, Company):
    """ Test to unset a user relation """
    brenard.company = None
    assert brenard.company_id is None

    # Retrieve EE company
    ee = ldap_client.get(Company, id='ee')
    assert isinstance(ee, Company)
    assert ee.id == 'ee'

    # Set brenard company as ee
    brenard.company = ee
    assert brenard.company_id == 'ee'


def test_user_change_and_restore(brenard):
    """ Test to change user lastname and restore it locally """
    user_orig_lastname = brenard.lastname
    brenard.lastname = 'Fox'   # pylint: disable=attribute-defined-outside-init
    assert brenard.restore()
    assert brenard.lastname == user_orig_lastname
    assert not brenard.is_modified()


def test_user_change_and_refresh(brenard):
    """ Test to change user lastname and refresh it from LDAP after """
    user_orig_lastname = brenard.lastname
    brenard.lastname = 'Fox'   # pylint: disable=attribute-defined-outside-init
    assert brenard.refresh()
    assert brenard.lastname == user_orig_lastname


def test_user_search_on_username_numid(brenard, ldap_client, User):
    """ Test to search user on username and numid """
    search = ldap_client.search(User, username=brenard.username, numid=brenard.numid)
    assert isinstance(search, LDAPSearch)
    assert search.filterstr == '(&(objectClass=top)(objectClass=inetOrgPerson)(objectClass=elPeople)(elNumId=4)(uid=brenard))'
    assert len(search) == 1
    assert brenard == search[0]


def test_user_create(ldap_client, User):
    """ Test to create a user """
    attrs = dict(
        username='jdoe',
        firstname='John',
        lastname='Doe',
        fullname='John Doe',
        mail='jdoe@eesyldap.org',
        start_date=datetime.datetime.now().date(),
        birth_date=datetime.date(1982, 2, 22),
        numid=55,
    )
    user = ldap_client.new(User, attrs)
    assert isinstance(user, User)
    assert user.save()

    # Verify that we can now find this user on LDAP server
    search = ldap_client.search(User, username=attrs['username'])
    assert len(search) == 1
    assert user == search[0]


def test_user_delete(ldap_client, jdoe, User):
    """ Test to delete a user """
    assert jdoe.delete()

    verify = ldap_client.search(User, username='jdoe')
    assert not verify


def test_user_delete_with_relation(ldap_client, brenard):
    """ Test to delete a user with relation """
    with pytest.raises(LDAPRequiredAttribute):
        brenard.delete()


def test_user_search_by_username_in(ldap_client, User, brenard, jdoe):
    """ Test to search users by username value in a list """
    usernames = [brenard.username, jdoe.username]
    search = ldap_client.search(User, username=usernames)
    assert isinstance(search, LDAPSearch)
    assert search.filterstr == '(&(objectClass=top)(objectClass=inetOrgPerson)(objectClass=elPeople)(|(uid=brenard)(uid=jdoe)))'
    assert len(search) == 2
    assert brenard in search and jdoe in search


def test_user_search_sorted(ldap_client, User, brenard, jdoe):
    """ Test to search users and sort its """
    usernames = [brenard.username, jdoe.username]
    result = ldap_client.search(User, username=usernames, sort_by='username')
    assert result[1] == jdoe


def test_user_search_sorted_reverse(ldap_client, User, brenard, jdoe):
    """ Test to search users and sort its """
    usernames = [brenard.username, jdoe.username]
    result = ldap_client.search(User, username=usernames, sort_by='username', sort_reverse=True)
    assert result[1] == brenard


def test_user_search_with_key_attr(ldap_client, User, brenard):
    """ Test to search users with a key attribute """
    result = ldap_client.search(User, username=brenard.username, key_attr='numid')
    assert result[brenard.numid] == brenard


def test_user_search_with_bad_key_attr(ldap_client, User):
    """ Test to search users and sort its """
    with pytest.raises(LDAPNotUniqueAttribute):
        ldap_client.search(User, key_attr='lastname')


def test_user_access_search_result_by_index(ldap_client, User, brenard, jdoe):
    """ Test to search users and access result by index """
    usernames = [brenard.username, jdoe.username]
    result = ldap_client.search(User, username=usernames, sort_by='username')

    assert result[0] == brenard
    assert jdoe in result[1:2]
    assert result[-1] == jdoe


def test_user_search_with_limit(ldap_client, User, brenard, jdoe):
    """ Test to search users with limit """
    usernames = [brenard.username, jdoe.username]
    result = ldap_client.search(User, username=usernames, limit=1)
    with pytest.raises(LDAPSearchLimitExceeded):
        result.first()


def test_user_search_with_hardlimit(ldap_client, User, brenard, jdoe):
    """ Test to search users with hardlimit """
    usernames = [brenard.username, jdoe.username]
    result = ldap_client.search(User, username=usernames, hardlimit=1)
    with pytest.raises(LDAPSearchHardLimitExceeded):
        result.first()


def test_user_search_by_specify_filter_after_creation(ldap_client, User):
    """ Test to search users by specify options after search creation """
    search = ldap_client.search(User)
    search.filter(enabled=True)
    search.filter(filterstr='(elNumId=*)')
    assert search.filterstr == '(&(objectClass=top)(objectClass=inetOrgPerson)(objectClass=elPeople)(elEnabled=TRUE)(elNumId=*))'


def test_user_affect_not_unique_username(brenard, jdoe):
    """ Test to affect a not unique username to user """
    with pytest.raises(LDAPAttributeUnicityError):
        brenard.username = jdoe.username
