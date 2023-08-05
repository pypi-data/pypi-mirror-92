# coding: utf-8
# Copyright (c) 2016, 2021, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class LogAnalyticsAssociatedEntity(object):
    """
    LogAnalyticsAssociatedEntity
    """

    def __init__(self, **kwargs):
        """
        Initializes a new LogAnalyticsAssociatedEntity object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param entity_id:
            The value to assign to the entity_id property of this LogAnalyticsAssociatedEntity.
        :type entity_id: str

        :param entity_name:
            The value to assign to the entity_name property of this LogAnalyticsAssociatedEntity.
        :type entity_name: str

        :param entity_type:
            The value to assign to the entity_type property of this LogAnalyticsAssociatedEntity.
        :type entity_type: str

        :param entity_type_display_name:
            The value to assign to the entity_type_display_name property of this LogAnalyticsAssociatedEntity.
        :type entity_type_display_name: str

        :param on_host:
            The value to assign to the on_host property of this LogAnalyticsAssociatedEntity.
        :type on_host: str

        :param association_count:
            The value to assign to the association_count property of this LogAnalyticsAssociatedEntity.
        :type association_count: int

        """
        self.swagger_types = {
            'entity_id': 'str',
            'entity_name': 'str',
            'entity_type': 'str',
            'entity_type_display_name': 'str',
            'on_host': 'str',
            'association_count': 'int'
        }

        self.attribute_map = {
            'entity_id': 'entityId',
            'entity_name': 'entityName',
            'entity_type': 'entityType',
            'entity_type_display_name': 'entityTypeDisplayName',
            'on_host': 'onHost',
            'association_count': 'associationCount'
        }

        self._entity_id = None
        self._entity_name = None
        self._entity_type = None
        self._entity_type_display_name = None
        self._on_host = None
        self._association_count = None

    @property
    def entity_id(self):
        """
        Gets the entity_id of this LogAnalyticsAssociatedEntity.
        entity guid


        :return: The entity_id of this LogAnalyticsAssociatedEntity.
        :rtype: str
        """
        return self._entity_id

    @entity_id.setter
    def entity_id(self, entity_id):
        """
        Sets the entity_id of this LogAnalyticsAssociatedEntity.
        entity guid


        :param entity_id: The entity_id of this LogAnalyticsAssociatedEntity.
        :type: str
        """
        self._entity_id = entity_id

    @property
    def entity_name(self):
        """
        Gets the entity_name of this LogAnalyticsAssociatedEntity.
        entity name


        :return: The entity_name of this LogAnalyticsAssociatedEntity.
        :rtype: str
        """
        return self._entity_name

    @entity_name.setter
    def entity_name(self, entity_name):
        """
        Sets the entity_name of this LogAnalyticsAssociatedEntity.
        entity name


        :param entity_name: The entity_name of this LogAnalyticsAssociatedEntity.
        :type: str
        """
        self._entity_name = entity_name

    @property
    def entity_type(self):
        """
        Gets the entity_type of this LogAnalyticsAssociatedEntity.
        entity type


        :return: The entity_type of this LogAnalyticsAssociatedEntity.
        :rtype: str
        """
        return self._entity_type

    @entity_type.setter
    def entity_type(self, entity_type):
        """
        Sets the entity_type of this LogAnalyticsAssociatedEntity.
        entity type


        :param entity_type: The entity_type of this LogAnalyticsAssociatedEntity.
        :type: str
        """
        self._entity_type = entity_type

    @property
    def entity_type_display_name(self):
        """
        Gets the entity_type_display_name of this LogAnalyticsAssociatedEntity.
        entity type display name


        :return: The entity_type_display_name of this LogAnalyticsAssociatedEntity.
        :rtype: str
        """
        return self._entity_type_display_name

    @entity_type_display_name.setter
    def entity_type_display_name(self, entity_type_display_name):
        """
        Sets the entity_type_display_name of this LogAnalyticsAssociatedEntity.
        entity type display name


        :param entity_type_display_name: The entity_type_display_name of this LogAnalyticsAssociatedEntity.
        :type: str
        """
        self._entity_type_display_name = entity_type_display_name

    @property
    def on_host(self):
        """
        Gets the on_host of this LogAnalyticsAssociatedEntity.
        on host


        :return: The on_host of this LogAnalyticsAssociatedEntity.
        :rtype: str
        """
        return self._on_host

    @on_host.setter
    def on_host(self, on_host):
        """
        Sets the on_host of this LogAnalyticsAssociatedEntity.
        on host


        :param on_host: The on_host of this LogAnalyticsAssociatedEntity.
        :type: str
        """
        self._on_host = on_host

    @property
    def association_count(self):
        """
        Gets the association_count of this LogAnalyticsAssociatedEntity.
        associationCount


        :return: The association_count of this LogAnalyticsAssociatedEntity.
        :rtype: int
        """
        return self._association_count

    @association_count.setter
    def association_count(self, association_count):
        """
        Sets the association_count of this LogAnalyticsAssociatedEntity.
        associationCount


        :param association_count: The association_count of this LogAnalyticsAssociatedEntity.
        :type: int
        """
        self._association_count = association_count

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
