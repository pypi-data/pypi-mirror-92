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

""" LDAP Object relations """

import logging

from eesyldap.exceptions import LDAPDuplicateObjectFound
from eesyldap.exceptions import LDAPRelationLinkAttributeValueMissing
from eesyldap.exceptions import LDAPRelatedObjectModifed

log = logging.getLogger(__name__)


class RelationOnLocalLinkAttribute:
    """
    LDAP object relation using local object link attribute

    This type of relation is based on a local attribute that stores one value (or more)
    that refers specifically to another object.
    """

    def __init__(self, obj_type, link_attr, link_attr_value='dn', key_attr=None,
                 reverse_name=None, reverse_multiple=True, reverse_key_attr=None):
        """
        Relation constructor

        :param  obj_type:           The related object type
        :param  link_attr:          The local link attribute name
        :param  link_attr_value:    The name of the attribute of the related object type whose value is stored by the
                                    link attribute (default: dn)
        :param  key_attr:           The name of the key attribute (on multiple relation = if the local link attribute
                                    is multiple)
        :param  reverse_name:       The name of the reversed relation to create on related object type (optinal)
        :param  reverse_multiple:   Boolean to define if the reversed relation is multiple
        :param  reverse_key_attr:   The key attribute of the reversed relation (if multiple)
        """
        self.obj_type = obj_type
        self.link_attr = link_attr
        self.link_attr_value = link_attr_value
        assert link_attr_value == 'dn' or obj_type.exists(link_attr_value), "%s : Object type %s have no attribute '%s' : " % (self, obj_type.__name__, link_attr_value)
        if key_attr is not None:
            assert key_attr == 'dn' or obj_type.exists(key_attr), "%s : Object type %s have no attribute '%s' : can't use it as key attribute" % (self, obj_type.__class__, key_attr)
            self.key_attr = key_attr
        else:
            self.key_attr = obj_type.get_rdn_attr() or 'dn'
        self.reverse_name = reverse_name
        self.reverse_multiple = reverse_multiple
        self.reverse_key_attr = reverse_key_attr

    def __repr__(self):
        """ Compute and return the “official” string representation of the relation object """
        return "<%s on %s=%s.%s>" % (self.__class__.__name__, self.link_attr, self.obj_type.__name__, self.link_attr_value)

    def add_reverse_relation(self, obj_type):
        """
        Add reverse relation if name is defined

        :param  obj_type:       The local object type
        """
        if self.reverse_name:
            reverse_relation = RelationOnRemoteLinkAttribute(
                obj_type=obj_type,
                link_attr=self.link_attr,
                link_attr_value=self.link_attr_value,
                multiple=self.reverse_multiple,
                key_attr=self.reverse_key_attr
            )
            log.debug('%s : Add reverse relation "%s" on %s object type : %s', self, self.reverse_name, self.obj_type.__name__, reverse_relation)
            self.obj_type.add_relation(self.reverse_name, reverse_relation)

    def _get_link_value(self, r_obj):
        """ Retreive the link value of a specific object and raise LDAPRelationLinkAttributeValueMissing
        if no link value is available """
        # Retreive and check related objetc link value
        link_value = getattr(r_obj, self.link_attr_value)
        if not link_value:
            raise LDAPRelationLinkAttributeValueMissing(self, r_obj)
        return link_value

    def get_related_objects(self, obj):
        """ Retreive related object(s) of a specific object """

        # Check that link attr exists
        assert obj.exists(self.link_attr), "%s : Object type %s have no attribute '%s' : " % (self, obj.__name__, self.link_attr)

        multiple = obj.is_multiple(self.link_attr)

        # Check link_attr_value
        link_values = getattr(obj, self.link_attr)
        if not link_values:
            log.debug('No link value retreive from "%s"', self.link_attr)
            return None if not multiple else dict()

        # If multiple, iter on link_values
        if multiple:
            result = dict()
            for link_value in link_values:
                identifiers = {self.link_attr_value: link_value}
                r_obj = obj.client.get(self.obj_type, **identifiers)
                if r_obj:
                    result[getattr(r_obj, self.key_attr) if self.key_attr else link_value] = r_obj
                else:
                    log.warning("%s : No %s related object found for %s=%s", self, self.obj_type.__name__, self.link_attr_value, link_value)
            return result

        # Otherwise :
        identifiers = {self.link_attr_value: link_values}
        return obj.client.get(self.obj_type, **identifiers)

    def set_related_objects(self, obj, related_objs):
        """
        Set related object of a specific object

        :param  obj:            The local object
        :param  related_objs:   The related objects : if the relation is multiple, it must be a dict as retreived by
                                the get_related_objects() method. If the relation is not multiple, it's must be an object
                                of the type of related object. In any case, it could be None (or an empty dict) to remove
                                all relations with current related objects.
        """
        # Check that link attr exists
        assert obj.exists(self.link_attr), "%s : Object type %s have no attribute '%s' : " % (self, obj.__name__, self.link_attr)

        # Verify that object is not modified
        if obj.is_modified():
            raise LDAPRelatedObjectModifed(self, obj)

        # If not related_objs, remove link attr
        if not related_objs:
            link_value = None
        elif obj.is_multiple(self.link_attr):
            # On multiple case
            assert isinstance(related_objs, dict), "%s : This relation is multiple : you must provide a dict of %s objects with %s attribute as key" % (self, self.obj_type.__name__, self.key_attr or 'default')
            link_value = []
            for r_obj_id, r_obj in related_objs.items():    # pylint: disable=unused-variable
                assert isinstance(r_obj, self.obj_type), "%s : You must provide a list of %s objects (%s provided)" % (self, self.obj_type.__name__, type(r_obj).__name__)

                # Check related object is not modified
                if r_obj.is_modified():
                    raise LDAPRelatedObjectModifed(self, r_obj)

                # Retreive and check related objetc link value
                r_obj_value = self._get_link_value(r_obj)

                link_value.append(r_obj_value)
        else:
            # On non-multiple case
            assert isinstance(related_objs, self.obj_type), "%s : You must provide a %s object (%s provided)" % (self, self.obj_type, type(related_objs).__name__)

            # Check related object is not modified
            if related_objs.is_modified():
                raise LDAPRelatedObjectModifed(self, related_objs)

            # Retreive and check related objetc link value
            link_value = self._get_link_value(related_objs)

        # Set link attribute on the local object
        setattr(obj, self.link_attr, link_value)
        return obj.save()

    def add_related_object(self, obj, r_obj, link_value=None):
        """
        Add a related object

        :param  obj:        The local object
        :param  r_obj:      The related object
        :param  link_value: The link value that refers to the related object (optional)
        """
        # Check that link attr exists
        assert obj.exists(self.link_attr), "%s : Object type %s have no attribute '%s' : " % (self, obj.__name__, self.link_attr)

        # Check object is not modified
        if obj.is_modified():
            raise LDAPRelatedObjectModifed(self, obj)

        # Check related object is not modified
        if r_obj.is_modified():
            raise LDAPRelatedObjectModifed(self, r_obj)

        # Retreive and check related objetc link value
        r_obj_value = self._get_link_value(r_obj)

        if obj.is_multiple(self.link_attr):
            link_value = getattr(obj, self.link_attr)
            if r_obj_value in link_value:
                # This relation already exists between obj and r_obj
                return True
            link_value.append(r_obj_value)
        else:
            link_value = r_obj_value

        # Set link attribute on the local object
        setattr(obj, self.link_attr, link_value)
        return obj.save()

    def remove_related_object(self, obj, r_obj, link_value=None):
        """
        Remove a related object

        :param  obj:        The local object
        :param  r_obj:      The related object
        :param  link_value: The link value that refers to the related object (optional)
        """
        # Check that link attr exists
        assert obj.exists(self.link_attr), "%s : Object type %s have no attribute '%s' : " % (self, obj.__name__, self.link_attr)

        # Check object is not modified
        if obj.is_modified():
            raise LDAPRelatedObjectModifed(self, obj)

        # Check related object is not modified
        if r_obj.is_modified():
            raise LDAPRelatedObjectModifed(self, r_obj)

        # Retreive and check related objetc link value
        r_obj_value = self._get_link_value(r_obj)

        if obj.is_multiple(self.link_attr):
            link_value = getattr(obj, self.link_attr)
            if r_obj_value not in link_value:
                # This relation does not exists between obj and r_obj
                return True
            link_value.remove(r_obj_value)
        else:
            link_value = None

        # Set link attribute on the local object
        setattr(obj, self.link_attr, link_value)
        return obj.save()

    def handle_object_changes(self, old_obj, new_obj):  # pylint: disable=unused-argument,no-self-use
        """
        Handle changes on object

        :param  old_obj:    The object in its state before modification
        :param  new_obj:    The object in its state after modification
        """
        # Link values are store on local object attributes, no changes need on related objects
        return True

    def handle_object_removal(self, obj):   # pylint: disable=unused-argument,no-self-use
        """
        Handle removal of object

        :param  obj:    The removed object
        """
        # Link values are store on local object attributes, no changes need on related objects
        return True


class RelationOnRemoteLinkAttribute:
    """
    LDAP object relation using remote object link attribute

    This type of relation is based on an attribute of the related objects that stores one value that
    refers specifically to the local object.
    """

    def __init__(self, obj_type, link_attr, link_attr_value='dn', multiple=True, key_attr=None,
                 reverse_name=None, reverse_key_attr=None):
        """
        Relation constructor

        :param  obj_type:           The related object type
        :param  link_attr:          The link attribute name on related object
        :param  link_attr_value:    The name of the local attribute whose value is stored by the link attribute
                                    of the related object type (default: dn)
        :param  multiple:           Boolean to define if the relation is multiple
        :param  key_attr:           The name of the key attribute (on multiple relation)
        :param  reverse_name:       The name of the reversed relation to create on related object type (optinal)
        :param  reverse_key_attr:   The key attribute of the reversed relation (if multiple)
        """
        self.obj_type = obj_type
        self.link_attr = link_attr
        self.link_attr_value = link_attr_value
        assert obj_type.exists(link_attr), "%s : Object type %s have no attribute '%s' : " % (self, obj_type.__name__, link_attr)
        self.multiple = multiple
        assert key_attr is None or not multiple, "%s : The key_attr could only be used with multiple relation" % self
        if key_attr is not None:
            assert key_attr == 'dn' or obj_type.exists(key_attr), "%s : Object type %s have no attribute '%s' : can't use it as key attribute" % (self, obj_type.__class__, key_attr)
            self.key_attr = key_attr
        else:
            self.key_attr = obj_type.get_rdn_attr() or 'dn'
        self.reverse_name = reverse_name
        self.reverse_key_attr = reverse_key_attr

    def add_reverse_relation(self, obj_type):
        """
        Add reverse relation if name is defined

        :param  obj_type:       The local object type
        """
        if self.reverse_name:
            reverse_relation = RelationOnLocalLinkAttribute(
                obj_type=obj_type,
                link_attr=self.link_attr,
                link_attr_value=self.link_attr_value,
                key_attr=self.reverse_key_attr
            )
            log.debug('%s : Add reverse relation "%s" on %s object type : %s', self, self.reverse_name, self.obj_type.__name__, reverse_relation)
            self.obj_type.add_relation(self.reverse_name, reverse_relation)

    def __repr__(self):
        """ Compute and return the “official” string representation of the relation object """
        return "<%s on %s.%s=%s>" % (self.__class__.__name__, self.obj_type.__name__, self.link_attr, self.link_attr_value)

    def _get_link_value(self, obj):
        """ Retreive the link value of a specific object and raise LDAPRelationLinkAttributeValueMissing
        if no link value is available """
        # Check link_attr_value
        assert self.link_attr_value == 'dn' or obj.exists(self.link_attr_value), "%s : Invalid link_attr_value '%s' provided in constructor" % (self, self.link_attr_value)
        link_value = getattr(obj, self.link_attr_value)
        if not link_value:
            raise LDAPRelationLinkAttributeValueMissing(self, obj)
        return link_value

    def get_related_objects(self, obj):
        """ Retreive related object(s) of a specific object """
        # Check link_attr_value
        assert self.link_attr_value == 'dn' or obj.exists(self.link_attr_value), "Invalid link_attr_value '%s' provided in constructor" % self.link_attr_value
        try:
            link_value = self._get_link_value(obj)
        except LDAPRelationLinkAttributeValueMissing:
            log.debug('No link value retreive from "%s"', self.link_attr_value)
            return None if not self.multiple else dict()

        # Composed search filters of related objects
        filters = {self.link_attr: link_value}

        # Run search
        result = obj.client.search(self.obj_type, key_attr=self.key_attr, **filters)

        # If multiple, return result or an empty dict()
        if self.multiple:
            return result

        # If not multiple, check result count
        if len(result) > 1:
            raise LDAPDuplicateObjectFound(self.obj_type)

        return result.first() if result else None

    def set_related_objects(self, obj, related_objs):
        """
        Set related object of a specific object

        :param  obj:            The local object
        :param  related_objs:   The related objects : if the relation is multiple, it must be a dict as retreived by
                                the get_related_objects() method. If the relation is not multiple, it's must be an object
                                of the type of related object. In any case, it could be None (or an empty dict) to remove
                                all relations with current related objects.
        """
        # Check link_attr_value
        assert self.link_attr_value == 'dn' or obj.exists(self.link_attr_value), "%s : Invalid link_attr_value '%s' provided in constructor" % (self, self.link_attr_value)
        link_value = self._get_link_value(obj)

        # Check object is not modified
        if obj.is_modified():
            raise LDAPRelatedObjectModifed(self, obj)

        # Retreive current list of related objects
        current_related_objects = self.get_related_objects(obj)

        # Check if no changes
        if related_objs == current_related_objects:
            log.debug('%s : no changes in related objects with %s', self, obj)
            return True

        # Init error flag
        error = False

        if self.multiple:
            # On multiple case
            assert isinstance(related_objs, dict), "%s : This relation is multiple : you must provide a dict of %s objects with %s attribute as key" % (self, self.obj_type.__name__, self.key_attr or 'defaut')

            # Iter on new related objects to add relation
            for r_obj_id, r_obj in related_objs.items():
                assert isinstance(r_obj, self.obj_type), "%s : You must provide a list of %s objects (%s provided)" % (self, self.obj_type.__name__, type(r_obj).__name__)
                log.debug('%s : Add relation between %s and %s', self, obj, r_obj)
                if not self.add_related_object(obj, r_obj, link_value=link_value):
                    error = True

            # Look for removed relation
            for r_obj_id, r_obj in current_related_objects.items():
                if r_obj_id not in related_objs:
                    log.debug('%s : Remove relation between %s and %s', self, obj, r_obj)
                    if not self.remove_related_object(obj, r_obj, link_value=link_value):
                        error = True
        else:
            # On non multiple case
            assert isinstance(related_objs, self.obj_type), "%s : You must provide a %s objects (%s provided)" % (self, self.obj_type.__name__, type(related_objs).__name__)

            if not self.add_related_object(obj, related_objs, link_value=link_value):
                error = True

            if not self.remove_related_object(obj, related_objs, link_value=link_value):
                error = True

        return not error

    def add_related_object(self, obj, r_obj, link_value=None):
        """
        Add a related object

        :param  obj:        The local object
        :param  r_obj:      The related object
        :param  link_value: The link value that refers to the local object (optional)
        """
        # Check related object is not modified
        if r_obj.is_modified():
            raise LDAPRelatedObjectModifed(self, r_obj)

        # Retreive link value
        link_value = self._get_link_value(obj) if link_value is None else link_value

        changed = False
        cur_value = getattr(r_obj, self.link_attr)
        if r_obj.is_multiple(self.link_attr):
            new_value = cur_value or []
            if link_value not in new_value:
                new_value.append(link_value)
                changed = True
        elif cur_value != link_value:
            new_value = link_value
            changed = True
        if changed:
            # Update remote object link attribute and save it
            log.debug('%s : %s -> %s', self, cur_value, new_value)
            setattr(r_obj, self.link_attr, new_value)
            if not r_obj.save():
                log.error("%s : An error occured updating attr %s of the object %s with values %s to link it with object %s", self, self.link_attr, r_obj, new_value, obj)
                return False
            log.debug('%s : Relation between %s and %s added', self, r_obj, obj)
        else:
            log.debug('%s : Object %s still in relation with %s', self, r_obj, obj)
        return True

    def remove_related_object(self, obj, r_obj, link_value=None):
        """
        Remove a related object

        :param  obj:        The local object
        :param  r_obj:      The related object
        :param  link_value: The link value that refers to the local object (optional)
        """
        # Retreive link value
        link_value = self._get_link_value(obj) if link_value is None else link_value

        if r_obj.is_multiple(self.link_attr):
            new_value = getattr(r_obj, self.link_attr) or []
            if link_value in new_value:
                new_value.remove(link_value)
        else:
            new_value = None
        # Update remote object link attribute and save it
        setattr(r_obj, self.link_attr, new_value)
        if not r_obj.save():
            log.error("%s : An error occured updating attr %s of the object %s with values %s to unlink it with object %s", self, self.link_attr, r_obj, new_value, obj)
            return False
        log.debug('%s : Relation between %s and %s removed', self, r_obj, obj)
        return True

    def rename_obj_on_related_object(self, obj, r_obj, old_link_value, new_link_value):
        """
        Rename object on related object link attribute

        :param  obj:            The local object
        :param  r_obj:          The related object
        :param  old_link_value: The old link value that refers to the local object
        :param  new_link_value: The new link value that refers to the local object
        """
        if r_obj.is_multiple(self.link_attr):
            new_value = getattr(r_obj, self.link_attr) or []
            new_value.remove(old_link_value)
            new_value.append(new_link_value)
        else:
            new_value = new_link_value
        # Update remote object link attribute and save it
        setattr(r_obj, self.link_attr, new_value)
        if not r_obj.save():
            log.error("%s : An error occured updating attr %s of the object %s with value %s to update link value of object %s from '%s' to '%s'", self, self.link_attr, r_obj, new_value, obj, old_link_value, new_link_value)
            return False
        log.debug('%s : object %s renamed on it relation with %s', self, obj, r_obj)
        return True

    def handle_object_changes(self, old_obj, new_obj):
        """
        Handle changes on object

        :param  old_obj:    The object in its state before modification
        :param  new_obj:    The object in its state after modification
        """

        # Retreive old link_value
        try:
            old_link_value = self._get_link_value(old_obj)
        except LDAPRelationLinkAttributeValueMissing:
            log.warning('No link value retreived from old object')
            return True

        # Retreive new link_value
        try:
            new_link_value = self._get_link_value(new_obj)
        except LDAPRelationLinkAttributeValueMissing:
            log.info('No link value retreived from new object : remove relation with related objects')

        # If no change, stop
        if old_link_value == new_link_value:
            log.debug('%s : No change detected on link value', self)
            return True

        log.debug('%s : change detected on link value : "%s" => "%s"', self, old_link_value, new_link_value)

        # Link modified : handle link_value change
        related_objs = self.get_related_objects(old_obj)
        if not related_objs:
            log.debug('%s : object %s is currently not link with other object', self, old_obj)
            return True

        if self.multiple:
            # On multiple relation case
            error = False
            for r_obj_id, r_obj in related_objs.items():    # pylint: disable=unused-variable
                if new_link_value is None:
                    if not self.remove_related_object(new_obj, r_obj, link_value=old_link_value):
                        error = True
                elif not self.rename_obj_on_related_object(new_obj, r_obj, old_link_value, new_link_value):
                    error = True
            return not error

        # On non multiple relation case
        if new_link_value is None:
            return self.remove_related_object(new_obj, related_objs, link_value=old_link_value)
        return self.rename_obj_on_related_object(new_obj, related_objs, old_link_value, new_link_value)

    def handle_object_removal(self, obj):
        """
        Handle removal of object

        :param  obj:    The removed object
        """
        # Retreive old link_value
        try:
            link_value = self._get_link_value(obj)
        except LDAPRelationLinkAttributeValueMissing:
            log.warning('No link value retreived from object')
            return True

        related_objs = self.get_related_objects(obj)
        if not related_objs:
            log.debug('%s : object %s is not link with other object', self, obj)
            return True
        log.debug('%s : object %s is link with some other object(s) : %s', self, obj, related_objs)

        if self.multiple:
            # On multiple relation case
            error = False
            for r_obj_id, r_obj in related_objs.items():    # pylint: disable=unused-variable
                if not self.remove_related_object(obj, r_obj, link_value=link_value):
                    error = True

            return not error

        # On non multiple relation case
        return self.remove_related_object(obj, related_objs, link_value=link_value)
