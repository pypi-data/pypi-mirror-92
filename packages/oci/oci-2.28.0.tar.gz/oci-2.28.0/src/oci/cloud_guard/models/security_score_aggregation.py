# coding: utf-8
# Copyright (c) 2016, 2021, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SecurityScoreAggregation(object):
    """
    Provides the dimensions and their corresponding count value.
    """

    #: A constant which can be used with the security_rating property of a SecurityScoreAggregation.
    #: This constant has a value of "EXCELLENT"
    SECURITY_RATING_EXCELLENT = "EXCELLENT"

    #: A constant which can be used with the security_rating property of a SecurityScoreAggregation.
    #: This constant has a value of "GOOD"
    SECURITY_RATING_GOOD = "GOOD"

    #: A constant which can be used with the security_rating property of a SecurityScoreAggregation.
    #: This constant has a value of "FAIR"
    SECURITY_RATING_FAIR = "FAIR"

    #: A constant which can be used with the security_rating property of a SecurityScoreAggregation.
    #: This constant has a value of "POOR"
    SECURITY_RATING_POOR = "POOR"

    def __init__(self, **kwargs):
        """
        Initializes a new SecurityScoreAggregation object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param dimensions_map:
            The value to assign to the dimensions_map property of this SecurityScoreAggregation.
        :type dimensions_map: dict(str, str)

        :param security_rating:
            The value to assign to the security_rating property of this SecurityScoreAggregation.
            Allowed values for this property are: "EXCELLENT", "GOOD", "FAIR", "POOR", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type security_rating: str

        :param security_score:
            The value to assign to the security_score property of this SecurityScoreAggregation.
        :type security_score: int

        """
        self.swagger_types = {
            'dimensions_map': 'dict(str, str)',
            'security_rating': 'str',
            'security_score': 'int'
        }

        self.attribute_map = {
            'dimensions_map': 'dimensionsMap',
            'security_rating': 'securityRating',
            'security_score': 'securityScore'
        }

        self._dimensions_map = None
        self._security_rating = None
        self._security_score = None

    @property
    def dimensions_map(self):
        """
        **[Required]** Gets the dimensions_map of this SecurityScoreAggregation.
        The key-value pairs of dimensions and their names.


        :return: The dimensions_map of this SecurityScoreAggregation.
        :rtype: dict(str, str)
        """
        return self._dimensions_map

    @dimensions_map.setter
    def dimensions_map(self, dimensions_map):
        """
        Sets the dimensions_map of this SecurityScoreAggregation.
        The key-value pairs of dimensions and their names.


        :param dimensions_map: The dimensions_map of this SecurityScoreAggregation.
        :type: dict(str, str)
        """
        self._dimensions_map = dimensions_map

    @property
    def security_rating(self):
        """
        **[Required]** Gets the security_rating of this SecurityScoreAggregation.
        The security rating with given dimension/s

        Allowed values for this property are: "EXCELLENT", "GOOD", "FAIR", "POOR", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The security_rating of this SecurityScoreAggregation.
        :rtype: str
        """
        return self._security_rating

    @security_rating.setter
    def security_rating(self, security_rating):
        """
        Sets the security_rating of this SecurityScoreAggregation.
        The security rating with given dimension/s


        :param security_rating: The security_rating of this SecurityScoreAggregation.
        :type: str
        """
        allowed_values = ["EXCELLENT", "GOOD", "FAIR", "POOR"]
        if not value_allowed_none_or_none_sentinel(security_rating, allowed_values):
            security_rating = 'UNKNOWN_ENUM_VALUE'
        self._security_rating = security_rating

    @property
    def security_score(self):
        """
        **[Required]** Gets the security_score of this SecurityScoreAggregation.
        The security score with given dimension/s


        :return: The security_score of this SecurityScoreAggregation.
        :rtype: int
        """
        return self._security_score

    @security_score.setter
    def security_score(self, security_score):
        """
        Sets the security_score of this SecurityScoreAggregation.
        The security score with given dimension/s


        :param security_score: The security_score of this SecurityScoreAggregation.
        :type: int
        """
        self._security_score = security_score

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
