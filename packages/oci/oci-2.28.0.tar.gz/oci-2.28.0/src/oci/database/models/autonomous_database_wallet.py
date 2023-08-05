# coding: utf-8
# Copyright (c) 2016, 2021, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AutonomousDatabaseWallet(object):
    """
    The Autonomous Database wallet details.
    """

    #: A constant which can be used with the lifecycle_state property of a AutonomousDatabaseWallet.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a AutonomousDatabaseWallet.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    def __init__(self, **kwargs):
        """
        Initializes a new AutonomousDatabaseWallet object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this AutonomousDatabaseWallet.
            Allowed values for this property are: "ACTIVE", "UPDATING", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param time_rotated:
            The value to assign to the time_rotated property of this AutonomousDatabaseWallet.
        :type time_rotated: datetime

        """
        self.swagger_types = {
            'lifecycle_state': 'str',
            'time_rotated': 'datetime'
        }

        self.attribute_map = {
            'lifecycle_state': 'lifecycleState',
            'time_rotated': 'timeRotated'
        }

        self._lifecycle_state = None
        self._time_rotated = None

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this AutonomousDatabaseWallet.
        The current lifecycle state of the Autonomous Database wallet.

        Allowed values for this property are: "ACTIVE", "UPDATING", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this AutonomousDatabaseWallet.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this AutonomousDatabaseWallet.
        The current lifecycle state of the Autonomous Database wallet.


        :param lifecycle_state: The lifecycle_state of this AutonomousDatabaseWallet.
        :type: str
        """
        allowed_values = ["ACTIVE", "UPDATING"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def time_rotated(self):
        """
        Gets the time_rotated of this AutonomousDatabaseWallet.
        The date and time the wallet was last rotated.


        :return: The time_rotated of this AutonomousDatabaseWallet.
        :rtype: datetime
        """
        return self._time_rotated

    @time_rotated.setter
    def time_rotated(self, time_rotated):
        """
        Sets the time_rotated of this AutonomousDatabaseWallet.
        The date and time the wallet was last rotated.


        :param time_rotated: The time_rotated of this AutonomousDatabaseWallet.
        :type: datetime
        """
        self._time_rotated = time_rotated

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
