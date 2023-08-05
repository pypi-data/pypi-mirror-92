# coding: utf-8
# Copyright (c) 2016, 2021, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UiParserTestMetadata(object):
    """
    UiParserTestMetadata
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UiParserTestMetadata object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param last_modified_time:
            The value to assign to the last_modified_time property of this UiParserTestMetadata.
        :type last_modified_time: str

        :param log_file_name:
            The value to assign to the log_file_name property of this UiParserTestMetadata.
        :type log_file_name: str

        :param time_zone:
            The value to assign to the time_zone property of this UiParserTestMetadata.
        :type time_zone: datetime

        """
        self.swagger_types = {
            'last_modified_time': 'str',
            'log_file_name': 'str',
            'time_zone': 'datetime'
        }

        self.attribute_map = {
            'last_modified_time': 'lastModifiedTime',
            'log_file_name': 'logFileName',
            'time_zone': 'timeZone'
        }

        self._last_modified_time = None
        self._log_file_name = None
        self._time_zone = None

    @property
    def last_modified_time(self):
        """
        Gets the last_modified_time of this UiParserTestMetadata.
        Last modified time


        :return: The last_modified_time of this UiParserTestMetadata.
        :rtype: str
        """
        return self._last_modified_time

    @last_modified_time.setter
    def last_modified_time(self, last_modified_time):
        """
        Sets the last_modified_time of this UiParserTestMetadata.
        Last modified time


        :param last_modified_time: The last_modified_time of this UiParserTestMetadata.
        :type: str
        """
        self._last_modified_time = last_modified_time

    @property
    def log_file_name(self):
        """
        Gets the log_file_name of this UiParserTestMetadata.
        Name of log file


        :return: The log_file_name of this UiParserTestMetadata.
        :rtype: str
        """
        return self._log_file_name

    @log_file_name.setter
    def log_file_name(self, log_file_name):
        """
        Sets the log_file_name of this UiParserTestMetadata.
        Name of log file


        :param log_file_name: The log_file_name of this UiParserTestMetadata.
        :type: str
        """
        self._log_file_name = log_file_name

    @property
    def time_zone(self):
        """
        Gets the time_zone of this UiParserTestMetadata.
        timeZone


        :return: The time_zone of this UiParserTestMetadata.
        :rtype: datetime
        """
        return self._time_zone

    @time_zone.setter
    def time_zone(self, time_zone):
        """
        Sets the time_zone of this UiParserTestMetadata.
        timeZone


        :param time_zone: The time_zone of this UiParserTestMetadata.
        :type: datetime
        """
        self._time_zone = time_zone

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
