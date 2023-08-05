# coding: utf-8
# Copyright (c) 2016, 2021, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateAutonomousContainerDatabaseDetails(object):
    """
    Describes the modification parameters for the Autonomous Container Database.
    """

    #: A constant which can be used with the patch_model property of a UpdateAutonomousContainerDatabaseDetails.
    #: This constant has a value of "RELEASE_UPDATES"
    PATCH_MODEL_RELEASE_UPDATES = "RELEASE_UPDATES"

    #: A constant which can be used with the patch_model property of a UpdateAutonomousContainerDatabaseDetails.
    #: This constant has a value of "RELEASE_UPDATE_REVISIONS"
    PATCH_MODEL_RELEASE_UPDATE_REVISIONS = "RELEASE_UPDATE_REVISIONS"

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateAutonomousContainerDatabaseDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this UpdateAutonomousContainerDatabaseDetails.
        :type display_name: str

        :param patch_model:
            The value to assign to the patch_model property of this UpdateAutonomousContainerDatabaseDetails.
            Allowed values for this property are: "RELEASE_UPDATES", "RELEASE_UPDATE_REVISIONS"
        :type patch_model: str

        :param maintenance_window_details:
            The value to assign to the maintenance_window_details property of this UpdateAutonomousContainerDatabaseDetails.
        :type maintenance_window_details: oci.database.models.MaintenanceWindow

        :param standby_maintenance_buffer_in_days:
            The value to assign to the standby_maintenance_buffer_in_days property of this UpdateAutonomousContainerDatabaseDetails.
        :type standby_maintenance_buffer_in_days: int

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateAutonomousContainerDatabaseDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateAutonomousContainerDatabaseDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param backup_config:
            The value to assign to the backup_config property of this UpdateAutonomousContainerDatabaseDetails.
        :type backup_config: oci.database.models.AutonomousContainerDatabaseBackupConfig

        """
        self.swagger_types = {
            'display_name': 'str',
            'patch_model': 'str',
            'maintenance_window_details': 'MaintenanceWindow',
            'standby_maintenance_buffer_in_days': 'int',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'backup_config': 'AutonomousContainerDatabaseBackupConfig'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'patch_model': 'patchModel',
            'maintenance_window_details': 'maintenanceWindowDetails',
            'standby_maintenance_buffer_in_days': 'standbyMaintenanceBufferInDays',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'backup_config': 'backupConfig'
        }

        self._display_name = None
        self._patch_model = None
        self._maintenance_window_details = None
        self._standby_maintenance_buffer_in_days = None
        self._freeform_tags = None
        self._defined_tags = None
        self._backup_config = None

    @property
    def display_name(self):
        """
        Gets the display_name of this UpdateAutonomousContainerDatabaseDetails.
        The display name for the Autonomous Container Database.


        :return: The display_name of this UpdateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this UpdateAutonomousContainerDatabaseDetails.
        The display name for the Autonomous Container Database.


        :param display_name: The display_name of this UpdateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def patch_model(self):
        """
        Gets the patch_model of this UpdateAutonomousContainerDatabaseDetails.
        Database Patch model preference.

        Allowed values for this property are: "RELEASE_UPDATES", "RELEASE_UPDATE_REVISIONS"


        :return: The patch_model of this UpdateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._patch_model

    @patch_model.setter
    def patch_model(self, patch_model):
        """
        Sets the patch_model of this UpdateAutonomousContainerDatabaseDetails.
        Database Patch model preference.


        :param patch_model: The patch_model of this UpdateAutonomousContainerDatabaseDetails.
        :type: str
        """
        allowed_values = ["RELEASE_UPDATES", "RELEASE_UPDATE_REVISIONS"]
        if not value_allowed_none_or_none_sentinel(patch_model, allowed_values):
            raise ValueError(
                "Invalid value for `patch_model`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._patch_model = patch_model

    @property
    def maintenance_window_details(self):
        """
        Gets the maintenance_window_details of this UpdateAutonomousContainerDatabaseDetails.

        :return: The maintenance_window_details of this UpdateAutonomousContainerDatabaseDetails.
        :rtype: oci.database.models.MaintenanceWindow
        """
        return self._maintenance_window_details

    @maintenance_window_details.setter
    def maintenance_window_details(self, maintenance_window_details):
        """
        Sets the maintenance_window_details of this UpdateAutonomousContainerDatabaseDetails.

        :param maintenance_window_details: The maintenance_window_details of this UpdateAutonomousContainerDatabaseDetails.
        :type: oci.database.models.MaintenanceWindow
        """
        self._maintenance_window_details = maintenance_window_details

    @property
    def standby_maintenance_buffer_in_days(self):
        """
        Gets the standby_maintenance_buffer_in_days of this UpdateAutonomousContainerDatabaseDetails.
        The scheduling detail for the quarterly maintenance window of the standby Autonomous Container Database.
        This value represents the number of days before schedlued maintenance of the primary database.


        :return: The standby_maintenance_buffer_in_days of this UpdateAutonomousContainerDatabaseDetails.
        :rtype: int
        """
        return self._standby_maintenance_buffer_in_days

    @standby_maintenance_buffer_in_days.setter
    def standby_maintenance_buffer_in_days(self, standby_maintenance_buffer_in_days):
        """
        Sets the standby_maintenance_buffer_in_days of this UpdateAutonomousContainerDatabaseDetails.
        The scheduling detail for the quarterly maintenance window of the standby Autonomous Container Database.
        This value represents the number of days before schedlued maintenance of the primary database.


        :param standby_maintenance_buffer_in_days: The standby_maintenance_buffer_in_days of this UpdateAutonomousContainerDatabaseDetails.
        :type: int
        """
        self._standby_maintenance_buffer_in_days = standby_maintenance_buffer_in_days

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateAutonomousContainerDatabaseDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this UpdateAutonomousContainerDatabaseDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateAutonomousContainerDatabaseDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this UpdateAutonomousContainerDatabaseDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateAutonomousContainerDatabaseDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this UpdateAutonomousContainerDatabaseDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateAutonomousContainerDatabaseDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this UpdateAutonomousContainerDatabaseDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def backup_config(self):
        """
        Gets the backup_config of this UpdateAutonomousContainerDatabaseDetails.

        :return: The backup_config of this UpdateAutonomousContainerDatabaseDetails.
        :rtype: oci.database.models.AutonomousContainerDatabaseBackupConfig
        """
        return self._backup_config

    @backup_config.setter
    def backup_config(self, backup_config):
        """
        Sets the backup_config of this UpdateAutonomousContainerDatabaseDetails.

        :param backup_config: The backup_config of this UpdateAutonomousContainerDatabaseDetails.
        :type: oci.database.models.AutonomousContainerDatabaseBackupConfig
        """
        self._backup_config = backup_config

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
