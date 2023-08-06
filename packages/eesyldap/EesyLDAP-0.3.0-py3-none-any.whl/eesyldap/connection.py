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

""" LDAP connection """

import logging
import time
import threading

import ldap
import ldap.modlist
from ldap import INVALID_CREDENTIALS        # pylint: disable=no-name-in-module
from ldap import SIZELIMIT_EXCEEDED         # pylint: disable=no-name-in-module

from eesyldap.exceptions import LDAPConnectionError
from eesyldap.exceptions import LDAPInvalidCredentials
from eesyldap.exceptions import LDAPSearchHardLimitExceeded
from eesyldap.exceptions import LDAPSearchLimitExceeded

log = logging.getLogger(__name__)


class LDAPConnection:
    """
    LDAP connection

    This class handle all LDAP connection stuff and locking problems.
    It's also implement helpers above python LDAP method to interact with LDAP server.

    param: config:  LDAP connection configuration as dict :

        - uri:              LDAP connection URI (required)
        - tls:              Enable TLS (optional, default: False)
        - base_dn:          Base DN (required)
        - bind_dn:          Bind DN (optional, default: annonymous connection)
        - bind_credential:  Bind credential (optional, default: annonymous connection)
        - timeout:          Operation and network connection timeout in seconds (optional, default: 2 seconds)
    """

    def __init__(self, config):
        self.config = config
        self.config['timeout'] = float(config['timeout']) if config.get('timeout') is not None else 2.0
        self.__lock = threading.Lock()
        self.con = None

    def __enter__(self):
        """ Acquire lock and bind on LDAP server """
        self.__lock.acquire()
        return self.bind(
            self.config.get('bind_dn'),
            self.config.get('bind_credential')
        )

    def __exit__(self, exit_type, value, traceback):
        """ Unbind on LDAP server and release lock """
        self.unbind()
        self.__lock.release()

    def bind(self, dn=None, credential=None, force=False):
        """ Initialize LDAP connection """

        if self.con is not None and not force:
            return True

        try:
            log.debug('Connect to LDAP server "%s"', self.config['uri'])
            self.con = ldap.initialize(self.config['uri'])

            log.debug('Set LDAP connection timeouts to %s second(s)', self.config['timeout'])
            self.con.set_option(ldap.OPT_NETWORK_TIMEOUT, self.config['timeout'])  # pylint: disable=no-member
            self.con.set_option(ldap.OPT_TIMEOUT, self.config['timeout'])          # pylint: disable=no-member
            self.con.set_option(ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3)          # pylint: disable=no-member

            if self.config.get('tls', 'false').lower() == 'true':
                self.con.start_tls_s()

            if dn and credential:
                log.debug('Bind on LDAP server "%s" with dn "%s"', self.config['uri'], dn)
                self.con.simple_bind_s(dn, credential)
            else:
                log.debug('No DN and password configured. Use annonymous connection.')

            return True
        except INVALID_CREDENTIALS:  # pylint: disable=no-member
            log.error('[LDAP] Authentication failed (%s)', dn)

            # Close the connection
            self.unbind()

            raise LDAPInvalidCredentials(self.config['uri'], dn)

        except Exception as err:
            log.error('Failed to connect to remote server', exc_info=1)

            # Close connection
            self.unbind()

            # Raise error
            raise LDAPConnectionError(self.config['uri'], str(err))

        return True

    def unbind(self):
        """ Unbind on LDAP connection """
        if self.con is None:
            return False

        try:
            self.con.unbind()

        except Exception:
            log.warning('Failed to unbind connection')
            return False

        finally:
            self.con = None

        return True

    @staticmethod
    def _get_scope(scope=None):
        """ Convert scope parameter value for python-ldap """
        if scope == 'sub' or scope is None:
            return ldap.SCOPE_SUBTREE   # pylint: disable=no-member
        if scope == 'one':
            return ldap.SCOPE_ONELEVEL  # pylint: disable=no-member
        if scope == 'base':
            return ldap.SCOPE_BASE      # pylint: disable=no-member
        raise Exception('Unknwon LDAP search scope %s' % scope)

    def search(self, base=None, filterstr='(objectClass=*)', scope=None, limit=None, hardlimit=None, **kwargs):
        """ LDAP search helper """
        if base is None:
            base = self.config.get('base_dn')
        if scope is None:
            scope = 'sub'
        log.debug('Run LDAP search with filter "%s" on base "%s" (scope = %s)', filterstr, base, scope)
        scope = self._get_scope(scope)
        sizelimit = 0 if hardlimit is None else int(hardlimit)
        try:
            start_time = time.time()
            result = self.con.search_ext_s(base, scope, filterstr=filterstr, sizelimit=sizelimit, **kwargs)
            log.debug('LDAP search result retreived in %.3f second(s)', (time.time() - start_time))
            # Ensure hard limit is handled
            if hardlimit and len(result) > hardlimit:
                raise LDAPSearchHardLimitExceeded(hardlimit)

            # Filter result to keep only items with DN (ignore references)
            result = [obj for obj in result if obj[0]]

            # Handle limit
            if limit and len(result) > limit:
                raise LDAPSearchLimitExceeded(limit)

            return result
        except SIZELIMIT_EXCEEDED:
            raise LDAPSearchHardLimitExceeded(sizelimit)

    def add(self, dn, modlist):
        """ LDAP add helper """
        return self.con.add_s(dn, modlist)

    def modify(self, dn, modlist, **kwargs):
        """ LDAP modify helper """
        return self.con.modify_s(dn, modlist, **kwargs)

    def rename(self, dn, new_rdn, **kwargs):
        """ LDAP modify helper """
        new_rdn = new_rdn.decode('utf-8') if isinstance(new_rdn, bytes) else new_rdn
        return self.con.rename_s(dn, new_rdn, **kwargs)

    def delete(self, dn):
        """ LDAP delete helper """
        return self.con.delete_s(dn)
