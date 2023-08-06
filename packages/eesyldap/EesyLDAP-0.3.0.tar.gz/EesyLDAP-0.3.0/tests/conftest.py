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

""" Test commons things """

import datetime
import logging
import pytest

import unidecode

from eesyldap.attributes import Boolean, Date, Datetime, Integer, JSON, Password, ShadowLastChange, Text
from eesyldap.object import LDAPObject
from eesyldap.relations import RelationOnRemoteLinkAttribute, RelationOnLocalLinkAttribute
from eesyldap.unicity import UniqueInDirectory, UniqueInSameObjectType

from tests.exceptions import CantReuseOldPassword
from tests.exceptions import CantReuseSamePassword

log = logging.getLogger(__name__)


@pytest.fixture
def ldap_client():
    """ Start fake LDAP server and retreive correponding LDAPClient object """
    from ldap_test import LdapServer
    from eesyldap.client import LDAPClient

    base_entry = {
        'objectclass': 'organization',
        'dn': 'o=eesyldap',
        'attributes': {
            'o': 'eesyldap'
        }
    }

    entries = [
        # People
        {
            'objectclass': 'organizationalUnit',
            'dn': 'ou=people,o=eesyldap',
            'attributes': {
                'ou': 'people'
            }
        },
        {
            'objectclass': ['elPeople', 'inetOrgPerson', 'top'],
            'dn': 'uid=brenard,ou=people,o=eesyldap',
            'attributes': {
                'uid': 'brenard',
                'givenName': 'Benjamin',
                'sn': 'Renard',
                'displayName': 'Benjamin Renard',
                'cn': 'Benjamin Renard',
                'userPassword': '{SSHA}dXJlDxG6YAVex1YmfP7wJD6bceYrJcQY',
                'mail': 'brenard@easter-eggs.com',
                'o': 'ee',
                'ou': ['admin', 'dev'],
                'elEnabled': 'TRUE',
                'elStartDate': '20061010000000Z',
                'elLastLogin': '20190704103725Z',
                'elBirthDate': '19861218000000Z',
                'elNumId': '4',
                'elbankdetails': '{"iban": "FR76 3000 3034 3900 0504 9292 376", "bic": "SOGEFRPP", "label": "defaut"}',
            }
        },

        # Companies
        {
            'objectclass': 'organizationalUnit',
            'dn': 'ou=companies,o=eesyldap',
            'attributes': {
                'ou': 'companies'
            }
        },
        {
            'objectclass': ['top', 'organization', 'elCompany'],
            'dn': 'o=ee,ou=companies,o=eesyldap',
            'attributes': {
                'o': 'ee',
                'cn': 'Easter-eggs',
                'mail': 'info@easter-eggs.com',
                'elNumId': '1',
                'manager': 'uid=brenard,ou=people,o=eesyldap',
            }
        },

        # Services
        {
            'objectclass': 'organizationalUnit',
            'dn': 'ou=services,o=eesyldap',
            'attributes': {
                'ou': 'services'
            }
        },
        {
            'objectclass': ['top', 'organizationalUnit', 'elService'],
            'dn': 'ou=admin,ou=services,o=eesyldap',
            'attributes': {
                'ou': 'admin',
                'cn': 'Admin Sys',
                'o': 'ee',
                'mail': 'admin@easter-eggs.com',
                'elNumId': '2',
                'manager': 'uid=brenard,ou=people,o=eesyldap'
            }
        },
        {
            'objectclass': ['top', 'organizationalUnit', 'elService'],
            'dn': 'ou=dev,ou=services,o=eesyldap',
            'attributes': {
                'ou': 'dev',
                'cn': 'Dev',
                'o': 'ee',
                'mail': 'dev@easter-eggs.com',
                'elNumId': '3',
                'manager': 'uid=brenard,ou=people,o=eesyldap'
            }
        },

        # Groups
        {
            'objectclass': 'organizationalUnit',
            'dn': 'ou=groups,o=eesyldap',
            'attributes': {
                'ou': 'groups'
            }
        },
        {
            'objectclass': ['top', 'elGroup'],
            'dn': 'cn=ldapsuperadmins,ou=groups,o=eesyldap',
            'attributes': {
                'cn': 'ldapsuperadmins',
                'description': 'Super admins of the LDAP directory',
                'memberuid': 'brenard',
                'o': 'ee',
                'uniquemember': 'uid=brenard,ou=people,o=eesyldap',
                'owner': 'uid=brenard,ou=people,o=eesyldap',
            }
        },
    ]

    server = LdapServer({
        'base': base_entry,
        'entries': entries,
    })

    server.start()

    # Initialize client
    ldap_config = {
        'uri': 'ldap://localhost:%d' % server.config['port'],
        'base_dn': base_entry['dn'],
        'bind_dn': server.config['bind_dn'],
        'bind_credential': server.config['password'],
        'user.base_dn': 'ou=people,%s' % base_entry['dn'],
        'user.scope': 'one',
        'company.base_dn': 'ou=companies,%s' % base_entry['dn'],
        'company.scope': 'one',
        'service.base_dn': 'ou=services,%s' % base_entry['dn'],
        'service.scope': 'one',
        'group.base_dn': 'ou=groups,%s' % base_entry['dn'],
        'group.scope': 'one',
    }

    cache_params = dict(
        cache_enabled=False,
        cache_type='memory',
        cache_expire=600
    )

    yield LDAPClient(ldap_config, **cache_params)

    server.stop()


@pytest.fixture(scope="session")
def Service():
    class Service(LDAPObject):
        """ Test Service object class """

        _class = ['top', 'organizationalUnit', 'elService']
        _attrs = {
            'id': Text('ou', unicity=UniqueInSameObjectType(), required=True),
            'name': Text('cn', required=True),
            'company_id': Text('o', required=True),
            'description': Text('description'),
            'mail': Text('mail', unicity=UniqueInDirectory()),
            'numid': Integer('elNumId', unicity=UniqueInDirectory()),
            'manager_dn': Text('manager'),
        }
        _rdn_ldap_attr = 'ou'
    return Service


@pytest.fixture(scope="session")
def User(Service):
    class User(LDAPObject):
        """ Test User object class """

        _class = ['top', 'inetOrgPerson', 'elPeople']
        _attrs = {
            'username': Text('uid', unicity=UniqueInSameObjectType(), required=True),
            'password': Password('userPassword', hash_type='ssha'),
            'password_historic': Text('elUserPasswordHistoric', multiple=True),
            'password_last_change': ShadowLastChange('shadowLastChange'),
            'firstname': Text('givenName', required=True),
            'lastname': Text('sn', required=True),
            'fullname': Text('displayName', required=True),
            'fullname_normalized': Text('cn', required=True),
            'mail': Text('mail', unicity=UniqueInDirectory()),
            'company_id': Text('o'),
            'service_ids': Text('ou', multiple=True),
            'enabled': Boolean('elEnabled'),
            'start_date': Date('elStartDate'),
            'end_date': Date('elEndDate'),
            'last_login': Datetime('elLastLogin'),
            'birth_date': Date('elBirthDate', naive=True),
            'numid': Integer('elNumId', unicity=UniqueInDirectory()),
            'bank_details': JSON('elBankDetails', unicity=UniqueInDirectory(), multiple=True),
        }
        _rdn_ldap_attr = 'uid'
        _relations = {
            'services': RelationOnLocalLinkAttribute(Service, 'service_ids', link_attr_value='id', reverse_name='users', reverse_multiple=True),
            'managed_services': RelationOnRemoteLinkAttribute(Service, 'manager_dn', link_attr_value='dn', multiple=True, reverse_name='manager'),
        }

        def __setattr__(self, name, value):
            """ Set an attribute value """
            if name == 'password' and value:
                self._check_new_password(value)

            if LDAPObject.__setattr__(self, name, value):
                if name in ['firstname', 'lastname']:
                    self.fullname = "%s %s" % (self.firstname, self.lastname)  # pylint: disable=attribute-defined-outside-init
                if name == 'fullname':
                    self.fullname_normalized = unidecode.unidecode(value)  # pylint: disable=attribute-defined-outside-init
            return True

        def _check_new_password(self, new_password):
            """ Check new password """
            # Check new password against current password
            current_password = self.password
            log.debug("Current password = %s", current_password)
            if not self.password:
                log.debug('User have no password')
            elif self.attrs.password.verify(new_password, current_password):
                log.warning('Try to reuse the same password as current one')
                raise CantReuseSamePassword(self.attrs.password.ldap_name, new_password)

            # Check new password against historic
            historic = self.password_historic
            if self.attrs.password.is_hashed_password(new_password):
                log.warning('New password is currently hashed : could not check it against historic')
            else:
                log.debug('Current password historic = %s', historic)
                for hashed_password in historic:
                    if self.attrs.password.verify(new_password, hashed_password):
                        log.warning('Try to reuse an old password')
                        raise CantReuseOldPassword(self.attrs.password.ldap_name, new_password)
                    log.debug('Password "%s" does not match with old one "%s"', new_password, hashed_password)

            log.debug('New user password is valid')

            # Add current password to historic
            if current_password:
                if len(historic) >= 3:
                    historic = historic[(len(historic) - 4):]
                if not self.attrs.password.is_hashed_password(current_password):
                    log.info('Current password is clear : hash it before inclusion in historic')
                    current_password = self.attrs.password.hash(current_password)
                if current_password not in historic:
                    historic.append(current_password)
                log.debug('New user password historic = %s', historic)
                self.password_historic = historic   # pylint: disable=attribute-defined-outside-init
            else:
                log.debug("Current user password not available : can't add it in historic")

            # Adjust password_last_change
            self.password_last_change = datetime.date.today()   # pylint: disable=attribute-defined-outside-init

    # Add reverse relations of User objects to Services
    User.add_reverse_relations()

    return User


@pytest.fixture(scope="session")
def Company(User, Service):
    class Company(LDAPObject):
        """ Test Company object class """

        _class = ['top', 'organization', 'elCompany']
        _attrs = {
            'id': Text('o', unicity=UniqueInSameObjectType(), required=True),
            'name': Text('cn', unicity=UniqueInSameObjectType(), required=True),
            'description': Text('description'),
            'mail': Text('mail', unicity=UniqueInDirectory()),
            'numid': Integer('elNumId', unicity=UniqueInDirectory()),
            'manager_dn': Text('manager', required=True),
        }
        _rdn_ldap_attr = 'o'

        _relations = {
            'manager': RelationOnLocalLinkAttribute(User, 'manager_dn', link_attr_value='dn', reverse_name='managed_company', reverse_multiple=False),
            'users': RelationOnRemoteLinkAttribute(User, 'company_id', link_attr_value='id', reverse_name='company'),
            'services': RelationOnRemoteLinkAttribute(Service, 'company_id', link_attr_value='id', reverse_name='company'),
        }

    # Add reverse relations of Company objects
    Company.add_reverse_relations()

    return Company


@pytest.fixture(scope="session")
def Group(User, Service, Company):
    class Group(LDAPObject):
        """ Test Group object class """
        _class = ['top', 'elGroup']
        _attrs = {
            'name': Text('cn', unicity=UniqueInSameObjectType(), required=True),
            'description': Text('description', required=True),
            'member_usernames': Text('memberUid', multiple=True),
            'member_dns': Text('uniqueMember', multiple=True),
            'company_id': Text('o'),
            'service_ids': Text('ou', multiple=True),
            'owner_dn': Text('owner'),
        }

        _rdn_attr = 'name'

        _relations = {
            'owner': RelationOnLocalLinkAttribute(User, 'owner_dn', link_attr_value='dn', reverse_name='owned_groups'),
            'members': RelationOnLocalLinkAttribute(User, 'member_dns', link_attr_value='dn', reverse_name='groups', reverse_multiple=True),
            'members_by_username': RelationOnLocalLinkAttribute(User, 'member_usernames', link_attr_value='username', reverse_name='groups_by_username', reverse_multiple=True),
            'company': RelationOnLocalLinkAttribute(Company, 'company_id', link_attr_value='id', reverse_name='groups'),
            'services': RelationOnLocalLinkAttribute(Service, 'service_ids', link_attr_value='id', reverse_name='groups'),
        }

        def __setattr__(self, name, value):
            """ Set an attribute value """
            if LDAPObject.__setattr__(self, name, value):
                if name == 'members':
                    self.members_by_username = dict(    # pylint: disable=attribute-defined-outside-init
                        (member.username, member)
                        for member_dn, member in value.items()
                    )
            return True

    # Add reverse relations of Group objects
    Group.add_reverse_relations()

    return Group


@pytest.fixture
def brenard(ldap_client, User):
    """ Retreive brenard user from LDAP """
    user = ldap_client.get(User, username='brenard')
    assert isinstance(user, User)
    assert user.username == 'brenard'

    return user


@pytest.fixture
def jdoe(ldap_client, User):
    """ Create jdoe user in LDAP """
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

    return user


@pytest.fixture
def ee(ldap_client, Company):
    """ Retreive ee company from LDAP """
    company = ldap_client.get(Company, id='ee')
    assert isinstance(company, Company)
    assert company.id == 'ee'

    return company


@pytest.fixture
def dev(ldap_client, Service):
    """ Retreive dev service from LDAP """
    service = ldap_client.get(Service, id='dev')
    assert isinstance(service, Service)
    assert service.id == 'dev'

    return service


@pytest.fixture
def admin(ldap_client, Service):
    """ Retreive admin service from LDAP """
    service = ldap_client.get(Service, id='admin')
    assert isinstance(service, Service)
    assert service.id == 'admin'

    return service


@pytest.fixture
def ldapsuperadmins(ldap_client, Group):
    """ Retreive admin service from LDAP """
    group = ldap_client.get(Group, name='ldapsuperadmins')
    assert isinstance(group, Group)
    assert group.name == 'ldapsuperadmins'

    return group
