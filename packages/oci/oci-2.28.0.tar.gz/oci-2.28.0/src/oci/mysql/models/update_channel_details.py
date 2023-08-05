# coding: utf-8
# Copyright (c) 2016, 2021, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateChannelDetails(object):
    """
    Details required to update a Channel
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateChannelDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param source:
            The value to assign to the source property of this UpdateChannelDetails.
        :type source: oci.mysql.models.UpdateChannelSourceDetails

        :param target:
            The value to assign to the target property of this UpdateChannelDetails.
        :type target: oci.mysql.models.UpdateChannelTargetDetails

        :param display_name:
            The value to assign to the display_name property of this UpdateChannelDetails.
        :type display_name: str

        :param is_enabled:
            The value to assign to the is_enabled property of this UpdateChannelDetails.
        :type is_enabled: bool

        :param description:
            The value to assign to the description property of this UpdateChannelDetails.
        :type description: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateChannelDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateChannelDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'source': 'UpdateChannelSourceDetails',
            'target': 'UpdateChannelTargetDetails',
            'display_name': 'str',
            'is_enabled': 'bool',
            'description': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'source': 'source',
            'target': 'target',
            'display_name': 'displayName',
            'is_enabled': 'isEnabled',
            'description': 'description',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._source = None
        self._target = None
        self._display_name = None
        self._is_enabled = None
        self._description = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def source(self):
        """
        Gets the source of this UpdateChannelDetails.

        :return: The source of this UpdateChannelDetails.
        :rtype: oci.mysql.models.UpdateChannelSourceDetails
        """
        return self._source

    @source.setter
    def source(self, source):
        """
        Sets the source of this UpdateChannelDetails.

        :param source: The source of this UpdateChannelDetails.
        :type: oci.mysql.models.UpdateChannelSourceDetails
        """
        self._source = source

    @property
    def target(self):
        """
        Gets the target of this UpdateChannelDetails.

        :return: The target of this UpdateChannelDetails.
        :rtype: oci.mysql.models.UpdateChannelTargetDetails
        """
        return self._target

    @target.setter
    def target(self, target):
        """
        Sets the target of this UpdateChannelDetails.

        :param target: The target of this UpdateChannelDetails.
        :type: oci.mysql.models.UpdateChannelTargetDetails
        """
        self._target = target

    @property
    def display_name(self):
        """
        Gets the display_name of this UpdateChannelDetails.
        The user-friendly name for the Channel. It does not have to be unique.


        :return: The display_name of this UpdateChannelDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this UpdateChannelDetails.
        The user-friendly name for the Channel. It does not have to be unique.


        :param display_name: The display_name of this UpdateChannelDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def is_enabled(self):
        """
        Gets the is_enabled of this UpdateChannelDetails.
        Whether the Channel should be enabled or disabled. Enabling a previously
        disabled Channel will cause the Channel to be started. Conversely, disabling
        a previously enabled Channel will stop the Channel. Both operations are
        executed asynchronously.


        :return: The is_enabled of this UpdateChannelDetails.
        :rtype: bool
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, is_enabled):
        """
        Sets the is_enabled of this UpdateChannelDetails.
        Whether the Channel should be enabled or disabled. Enabling a previously
        disabled Channel will cause the Channel to be started. Conversely, disabling
        a previously enabled Channel will stop the Channel. Both operations are
        executed asynchronously.


        :param is_enabled: The is_enabled of this UpdateChannelDetails.
        :type: bool
        """
        self._is_enabled = is_enabled

    @property
    def description(self):
        """
        Gets the description of this UpdateChannelDetails.
        User provided description of the Channel.


        :return: The description of this UpdateChannelDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this UpdateChannelDetails.
        User provided description of the Channel.


        :param description: The description of this UpdateChannelDetails.
        :type: str
        """
        self._description = description

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateChannelDetails.
        Simple key-value pair applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this UpdateChannelDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateChannelDetails.
        Simple key-value pair applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this UpdateChannelDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateChannelDetails.
        Usage of predefined tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this UpdateChannelDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateChannelDetails.
        Usage of predefined tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this UpdateChannelDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
