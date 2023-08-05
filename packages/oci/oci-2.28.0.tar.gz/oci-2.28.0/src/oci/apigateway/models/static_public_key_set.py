# coding: utf-8
# Copyright (c) 2016, 2021, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .public_key_set import PublicKeySet
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class StaticPublicKeySet(PublicKeySet):
    """
    A set of static public keys that will be used to verify the JWT signature.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new StaticPublicKeySet object with values from keyword arguments. The default value of the :py:attr:`~oci.apigateway.models.StaticPublicKeySet.type` attribute
        of this class is ``STATIC_KEYS`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this StaticPublicKeySet.
            Allowed values for this property are: "STATIC_KEYS", "REMOTE_JWKS"
        :type type: str

        :param keys:
            The value to assign to the keys property of this StaticPublicKeySet.
        :type keys: list[oci.apigateway.models.StaticPublicKey]

        """
        self.swagger_types = {
            'type': 'str',
            'keys': 'list[StaticPublicKey]'
        }

        self.attribute_map = {
            'type': 'type',
            'keys': 'keys'
        }

        self._type = None
        self._keys = None
        self._type = 'STATIC_KEYS'

    @property
    def keys(self):
        """
        Gets the keys of this StaticPublicKeySet.
        The set of static public keys.


        :return: The keys of this StaticPublicKeySet.
        :rtype: list[oci.apigateway.models.StaticPublicKey]
        """
        return self._keys

    @keys.setter
    def keys(self, keys):
        """
        Sets the keys of this StaticPublicKeySet.
        The set of static public keys.


        :param keys: The keys of this StaticPublicKeySet.
        :type: list[oci.apigateway.models.StaticPublicKey]
        """
        self._keys = keys

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
