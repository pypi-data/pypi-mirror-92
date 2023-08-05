# coding: utf-8
# Copyright (c) 2016, 2021, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class WorkRequestError(object):
    """
    A Data Flow work request error object.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new WorkRequestError object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param code:
            The value to assign to the code property of this WorkRequestError.
        :type code: str

        :param id:
            The value to assign to the id property of this WorkRequestError.
        :type id: int

        :param message:
            The value to assign to the message property of this WorkRequestError.
        :type message: str

        :param timestamp:
            The value to assign to the timestamp property of this WorkRequestError.
        :type timestamp: datetime

        :param work_requestid:
            The value to assign to the work_requestid property of this WorkRequestError.
        :type work_requestid: str

        """
        self.swagger_types = {
            'code': 'str',
            'id': 'int',
            'message': 'str',
            'timestamp': 'datetime',
            'work_requestid': 'str'
        }

        self.attribute_map = {
            'code': 'code',
            'id': 'id',
            'message': 'message',
            'timestamp': 'timestamp',
            'work_requestid': 'workRequestid'
        }

        self._code = None
        self._id = None
        self._message = None
        self._timestamp = None
        self._work_requestid = None

    @property
    def code(self):
        """
        **[Required]** Gets the code of this WorkRequestError.
        A Machine-usable code for the error that occured.


        :return: The code of this WorkRequestError.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """
        Sets the code of this WorkRequestError.
        A Machine-usable code for the error that occured.


        :param code: The code of this WorkRequestError.
        :type: str
        """
        self._code = code

    @property
    def id(self):
        """
        Gets the id of this WorkRequestError.
        The id of a work request error.


        :return: The id of this WorkRequestError.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this WorkRequestError.
        The id of a work request error.


        :param id: The id of this WorkRequestError.
        :type: int
        """
        self._id = id

    @property
    def message(self):
        """
        **[Required]** Gets the message of this WorkRequestError.
        A human readable description of the issue encountered.


        :return: The message of this WorkRequestError.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this WorkRequestError.
        A human readable description of the issue encountered.


        :param message: The message of this WorkRequestError.
        :type: str
        """
        self._message = message

    @property
    def timestamp(self):
        """
        **[Required]** Gets the timestamp of this WorkRequestError.
        The time the error occured. An RFC3339 formatted datetime string.


        :return: The timestamp of this WorkRequestError.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Sets the timestamp of this WorkRequestError.
        The time the error occured. An RFC3339 formatted datetime string.


        :param timestamp: The timestamp of this WorkRequestError.
        :type: datetime
        """
        self._timestamp = timestamp

    @property
    def work_requestid(self):
        """
        Gets the work_requestid of this WorkRequestError.
        The OCID of a work request.


        :return: The work_requestid of this WorkRequestError.
        :rtype: str
        """
        return self._work_requestid

    @work_requestid.setter
    def work_requestid(self, work_requestid):
        """
        Sets the work_requestid of this WorkRequestError.
        The OCID of a work request.


        :param work_requestid: The work_requestid of this WorkRequestError.
        :type: str
        """
        self._work_requestid = work_requestid

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
