# coding: utf-8
# Copyright (c) 2016, 2021, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .instance_agent_command_output_details import InstanceAgentCommandOutputDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class InstanceAgentCommandOutputViaObjectStorageTupleDetails(InstanceAgentCommandOutputDetails):
    """
    Command output via object storage tuple.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new InstanceAgentCommandOutputViaObjectStorageTupleDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.compute_instance_agent.models.InstanceAgentCommandOutputViaObjectStorageTupleDetails.output_type` attribute
        of this class is ``OBJECT_STORAGE_TUPLE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param output_type:
            The value to assign to the output_type property of this InstanceAgentCommandOutputViaObjectStorageTupleDetails.
            Allowed values for this property are: "TEXT", "OBJECT_STORAGE_URI", "OBJECT_STORAGE_TUPLE"
        :type output_type: str

        :param bucket_name:
            The value to assign to the bucket_name property of this InstanceAgentCommandOutputViaObjectStorageTupleDetails.
        :type bucket_name: str

        :param namespace_name:
            The value to assign to the namespace_name property of this InstanceAgentCommandOutputViaObjectStorageTupleDetails.
        :type namespace_name: str

        :param object_name:
            The value to assign to the object_name property of this InstanceAgentCommandOutputViaObjectStorageTupleDetails.
        :type object_name: str

        """
        self.swagger_types = {
            'output_type': 'str',
            'bucket_name': 'str',
            'namespace_name': 'str',
            'object_name': 'str'
        }

        self.attribute_map = {
            'output_type': 'outputType',
            'bucket_name': 'bucketName',
            'namespace_name': 'namespaceName',
            'object_name': 'objectName'
        }

        self._output_type = None
        self._bucket_name = None
        self._namespace_name = None
        self._object_name = None
        self._output_type = 'OBJECT_STORAGE_TUPLE'

    @property
    def bucket_name(self):
        """
        **[Required]** Gets the bucket_name of this InstanceAgentCommandOutputViaObjectStorageTupleDetails.
        The Object Storage bucket for the command output.


        :return: The bucket_name of this InstanceAgentCommandOutputViaObjectStorageTupleDetails.
        :rtype: str
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name):
        """
        Sets the bucket_name of this InstanceAgentCommandOutputViaObjectStorageTupleDetails.
        The Object Storage bucket for the command output.


        :param bucket_name: The bucket_name of this InstanceAgentCommandOutputViaObjectStorageTupleDetails.
        :type: str
        """
        self._bucket_name = bucket_name

    @property
    def namespace_name(self):
        """
        **[Required]** Gets the namespace_name of this InstanceAgentCommandOutputViaObjectStorageTupleDetails.
        The Object Storage namespace for the command output.


        :return: The namespace_name of this InstanceAgentCommandOutputViaObjectStorageTupleDetails.
        :rtype: str
        """
        return self._namespace_name

    @namespace_name.setter
    def namespace_name(self, namespace_name):
        """
        Sets the namespace_name of this InstanceAgentCommandOutputViaObjectStorageTupleDetails.
        The Object Storage namespace for the command output.


        :param namespace_name: The namespace_name of this InstanceAgentCommandOutputViaObjectStorageTupleDetails.
        :type: str
        """
        self._namespace_name = namespace_name

    @property
    def object_name(self):
        """
        **[Required]** Gets the object_name of this InstanceAgentCommandOutputViaObjectStorageTupleDetails.
        The Object Storage name for the command output.


        :return: The object_name of this InstanceAgentCommandOutputViaObjectStorageTupleDetails.
        :rtype: str
        """
        return self._object_name

    @object_name.setter
    def object_name(self, object_name):
        """
        Sets the object_name of this InstanceAgentCommandOutputViaObjectStorageTupleDetails.
        The Object Storage name for the command output.


        :param object_name: The object_name of this InstanceAgentCommandOutputViaObjectStorageTupleDetails.
        :type: str
        """
        self._object_name = object_name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
