# coding: utf-8
# Copyright (c) 2016, 2021, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MetricThresholdRule(object):
    """
    An autoscaling action is triggered when a performance metric meets or exceeds a threshold
    """

    #: A constant which can be used with the operator property of a MetricThresholdRule.
    #: This constant has a value of "GT"
    OPERATOR_GT = "GT"

    #: A constant which can be used with the operator property of a MetricThresholdRule.
    #: This constant has a value of "LT"
    OPERATOR_LT = "LT"

    def __init__(self, **kwargs):
        """
        Initializes a new MetricThresholdRule object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param duration_in_minutes:
            The value to assign to the duration_in_minutes property of this MetricThresholdRule.
        :type duration_in_minutes: int

        :param operator:
            The value to assign to the operator property of this MetricThresholdRule.
            Allowed values for this property are: "GT", "LT", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type operator: str

        :param value:
            The value to assign to the value property of this MetricThresholdRule.
        :type value: int

        """
        self.swagger_types = {
            'duration_in_minutes': 'int',
            'operator': 'str',
            'value': 'int'
        }

        self.attribute_map = {
            'duration_in_minutes': 'durationInMinutes',
            'operator': 'operator',
            'value': 'value'
        }

        self._duration_in_minutes = None
        self._operator = None
        self._value = None

    @property
    def duration_in_minutes(self):
        """
        **[Required]** Gets the duration_in_minutes of this MetricThresholdRule.
        This value is the minimum period of time metric value meets or exceeds threshold value before action is trigger. The value is in minutes.


        :return: The duration_in_minutes of this MetricThresholdRule.
        :rtype: int
        """
        return self._duration_in_minutes

    @duration_in_minutes.setter
    def duration_in_minutes(self, duration_in_minutes):
        """
        Sets the duration_in_minutes of this MetricThresholdRule.
        This value is the minimum period of time metric value meets or exceeds threshold value before action is trigger. The value is in minutes.


        :param duration_in_minutes: The duration_in_minutes of this MetricThresholdRule.
        :type: int
        """
        self._duration_in_minutes = duration_in_minutes

    @property
    def operator(self):
        """
        **[Required]** Gets the operator of this MetricThresholdRule.
        The comparison operator to use. Options are greater than (GT), less than (LT).

        Allowed values for this property are: "GT", "LT", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The operator of this MetricThresholdRule.
        :rtype: str
        """
        return self._operator

    @operator.setter
    def operator(self, operator):
        """
        Sets the operator of this MetricThresholdRule.
        The comparison operator to use. Options are greater than (GT), less than (LT).


        :param operator: The operator of this MetricThresholdRule.
        :type: str
        """
        allowed_values = ["GT", "LT"]
        if not value_allowed_none_or_none_sentinel(operator, allowed_values):
            operator = 'UNKNOWN_ENUM_VALUE'
        self._operator = operator

    @property
    def value(self):
        """
        **[Required]** Gets the value of this MetricThresholdRule.
        integer non negative value. 0 < value < 100


        :return: The value of this MetricThresholdRule.
        :rtype: int
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this MetricThresholdRule.
        integer non negative value. 0 < value < 100


        :param value: The value of this MetricThresholdRule.
        :type: int
        """
        self._value = value

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
