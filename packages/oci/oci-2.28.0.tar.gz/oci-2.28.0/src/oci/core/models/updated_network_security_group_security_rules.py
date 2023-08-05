# coding: utf-8
# Copyright (c) 2016, 2021, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdatedNetworkSecurityGroupSecurityRules(object):
    """
    UpdatedNetworkSecurityGroupSecurityRules model.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdatedNetworkSecurityGroupSecurityRules object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param security_rules:
            The value to assign to the security_rules property of this UpdatedNetworkSecurityGroupSecurityRules.
        :type security_rules: list[oci.core.models.SecurityRule]

        """
        self.swagger_types = {
            'security_rules': 'list[SecurityRule]'
        }

        self.attribute_map = {
            'security_rules': 'securityRules'
        }

        self._security_rules = None

    @property
    def security_rules(self):
        """
        Gets the security_rules of this UpdatedNetworkSecurityGroupSecurityRules.
        The NSG security rules that were updated.


        :return: The security_rules of this UpdatedNetworkSecurityGroupSecurityRules.
        :rtype: list[oci.core.models.SecurityRule]
        """
        return self._security_rules

    @security_rules.setter
    def security_rules(self, security_rules):
        """
        Sets the security_rules of this UpdatedNetworkSecurityGroupSecurityRules.
        The NSG security rules that were updated.


        :param security_rules: The security_rules of this UpdatedNetworkSecurityGroupSecurityRules.
        :type: list[oci.core.models.SecurityRule]
        """
        self._security_rules = security_rules

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
