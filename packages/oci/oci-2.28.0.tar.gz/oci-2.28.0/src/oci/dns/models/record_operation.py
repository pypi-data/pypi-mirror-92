# coding: utf-8
# Copyright (c) 2016, 2021, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RecordOperation(object):
    """
    An extension of the existing record resource, describing either a
    precondition, an add, or a remove. Preconditions check all fields,
    including read-only data like `recordHash` and `rrsetVersion`.
    """

    #: A constant which can be used with the operation property of a RecordOperation.
    #: This constant has a value of "REQUIRE"
    OPERATION_REQUIRE = "REQUIRE"

    #: A constant which can be used with the operation property of a RecordOperation.
    #: This constant has a value of "PROHIBIT"
    OPERATION_PROHIBIT = "PROHIBIT"

    #: A constant which can be used with the operation property of a RecordOperation.
    #: This constant has a value of "ADD"
    OPERATION_ADD = "ADD"

    #: A constant which can be used with the operation property of a RecordOperation.
    #: This constant has a value of "REMOVE"
    OPERATION_REMOVE = "REMOVE"

    def __init__(self, **kwargs):
        """
        Initializes a new RecordOperation object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param domain:
            The value to assign to the domain property of this RecordOperation.
        :type domain: str

        :param record_hash:
            The value to assign to the record_hash property of this RecordOperation.
        :type record_hash: str

        :param is_protected:
            The value to assign to the is_protected property of this RecordOperation.
        :type is_protected: bool

        :param rdata:
            The value to assign to the rdata property of this RecordOperation.
        :type rdata: str

        :param rrset_version:
            The value to assign to the rrset_version property of this RecordOperation.
        :type rrset_version: str

        :param rtype:
            The value to assign to the rtype property of this RecordOperation.
        :type rtype: str

        :param ttl:
            The value to assign to the ttl property of this RecordOperation.
        :type ttl: int

        :param operation:
            The value to assign to the operation property of this RecordOperation.
            Allowed values for this property are: "REQUIRE", "PROHIBIT", "ADD", "REMOVE"
        :type operation: str

        """
        self.swagger_types = {
            'domain': 'str',
            'record_hash': 'str',
            'is_protected': 'bool',
            'rdata': 'str',
            'rrset_version': 'str',
            'rtype': 'str',
            'ttl': 'int',
            'operation': 'str'
        }

        self.attribute_map = {
            'domain': 'domain',
            'record_hash': 'recordHash',
            'is_protected': 'isProtected',
            'rdata': 'rdata',
            'rrset_version': 'rrsetVersion',
            'rtype': 'rtype',
            'ttl': 'ttl',
            'operation': 'operation'
        }

        self._domain = None
        self._record_hash = None
        self._is_protected = None
        self._rdata = None
        self._rrset_version = None
        self._rtype = None
        self._ttl = None
        self._operation = None

    @property
    def domain(self):
        """
        Gets the domain of this RecordOperation.
        The fully qualified domain name where the record can be located.


        :return: The domain of this RecordOperation.
        :rtype: str
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """
        Sets the domain of this RecordOperation.
        The fully qualified domain name where the record can be located.


        :param domain: The domain of this RecordOperation.
        :type: str
        """
        self._domain = domain

    @property
    def record_hash(self):
        """
        Gets the record_hash of this RecordOperation.
        A unique identifier for the record within its zone.


        :return: The record_hash of this RecordOperation.
        :rtype: str
        """
        return self._record_hash

    @record_hash.setter
    def record_hash(self, record_hash):
        """
        Sets the record_hash of this RecordOperation.
        A unique identifier for the record within its zone.


        :param record_hash: The record_hash of this RecordOperation.
        :type: str
        """
        self._record_hash = record_hash

    @property
    def is_protected(self):
        """
        Gets the is_protected of this RecordOperation.
        A Boolean flag indicating whether or not parts of the record
        are unable to be explicitly managed.


        :return: The is_protected of this RecordOperation.
        :rtype: bool
        """
        return self._is_protected

    @is_protected.setter
    def is_protected(self, is_protected):
        """
        Sets the is_protected of this RecordOperation.
        A Boolean flag indicating whether or not parts of the record
        are unable to be explicitly managed.


        :param is_protected: The is_protected of this RecordOperation.
        :type: bool
        """
        self._is_protected = is_protected

    @property
    def rdata(self):
        """
        Gets the rdata of this RecordOperation.
        The record's data, as whitespace-delimited tokens in
        type-specific presentation format. All RDATA is normalized and the
        returned presentation of your RDATA may differ from its initial input.
        For more information about RDATA, see `Supported DNS Resource Record Types`__

        __ https://docs.cloud.oracle.com/iaas/Content/DNS/Reference/supporteddnsresource.htm


        :return: The rdata of this RecordOperation.
        :rtype: str
        """
        return self._rdata

    @rdata.setter
    def rdata(self, rdata):
        """
        Sets the rdata of this RecordOperation.
        The record's data, as whitespace-delimited tokens in
        type-specific presentation format. All RDATA is normalized and the
        returned presentation of your RDATA may differ from its initial input.
        For more information about RDATA, see `Supported DNS Resource Record Types`__

        __ https://docs.cloud.oracle.com/iaas/Content/DNS/Reference/supporteddnsresource.htm


        :param rdata: The rdata of this RecordOperation.
        :type: str
        """
        self._rdata = rdata

    @property
    def rrset_version(self):
        """
        Gets the rrset_version of this RecordOperation.
        The latest version of the record's zone in which its RRSet differs
        from the preceding version.


        :return: The rrset_version of this RecordOperation.
        :rtype: str
        """
        return self._rrset_version

    @rrset_version.setter
    def rrset_version(self, rrset_version):
        """
        Sets the rrset_version of this RecordOperation.
        The latest version of the record's zone in which its RRSet differs
        from the preceding version.


        :param rrset_version: The rrset_version of this RecordOperation.
        :type: str
        """
        self._rrset_version = rrset_version

    @property
    def rtype(self):
        """
        Gets the rtype of this RecordOperation.
        The type of DNS record, such as A or CNAME. For more information, see `Resource Record (RR) TYPEs`__.

        __ https://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml#dns-parameters-4


        :return: The rtype of this RecordOperation.
        :rtype: str
        """
        return self._rtype

    @rtype.setter
    def rtype(self, rtype):
        """
        Sets the rtype of this RecordOperation.
        The type of DNS record, such as A or CNAME. For more information, see `Resource Record (RR) TYPEs`__.

        __ https://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml#dns-parameters-4


        :param rtype: The rtype of this RecordOperation.
        :type: str
        """
        self._rtype = rtype

    @property
    def ttl(self):
        """
        Gets the ttl of this RecordOperation.
        The Time To Live for the record, in seconds.


        :return: The ttl of this RecordOperation.
        :rtype: int
        """
        return self._ttl

    @ttl.setter
    def ttl(self, ttl):
        """
        Sets the ttl of this RecordOperation.
        The Time To Live for the record, in seconds.


        :param ttl: The ttl of this RecordOperation.
        :type: int
        """
        self._ttl = ttl

    @property
    def operation(self):
        """
        Gets the operation of this RecordOperation.
        A description of how a record relates to a PATCH operation.


        - `REQUIRE` indicates a precondition that record data **must** already exist.
        - `PROHIBIT` indicates a precondition that record data **must not** already exist.
        - `ADD` indicates that record data **must** exist after successful application.
        - `REMOVE` indicates that record data **must not** exist after successful application.


          **Note:** `ADD` and `REMOVE` operations can succeed even if
          they require no changes when applied, such as when the described
          records are already present or absent.


          **Note:** `ADD` and `REMOVE` operations can describe changes for
          more than one record.


          **Example:** `{ \"domain\": \"www.example.com\", \"rtype\": \"AAAA\", \"ttl\": 60 }`
          specifies a new TTL for every record in the www.example.com AAAA RRSet.

        Allowed values for this property are: "REQUIRE", "PROHIBIT", "ADD", "REMOVE"


        :return: The operation of this RecordOperation.
        :rtype: str
        """
        return self._operation

    @operation.setter
    def operation(self, operation):
        """
        Sets the operation of this RecordOperation.
        A description of how a record relates to a PATCH operation.


        - `REQUIRE` indicates a precondition that record data **must** already exist.
        - `PROHIBIT` indicates a precondition that record data **must not** already exist.
        - `ADD` indicates that record data **must** exist after successful application.
        - `REMOVE` indicates that record data **must not** exist after successful application.


          **Note:** `ADD` and `REMOVE` operations can succeed even if
          they require no changes when applied, such as when the described
          records are already present or absent.


          **Note:** `ADD` and `REMOVE` operations can describe changes for
          more than one record.


          **Example:** `{ \"domain\": \"www.example.com\", \"rtype\": \"AAAA\", \"ttl\": 60 }`
          specifies a new TTL for every record in the www.example.com AAAA RRSet.


        :param operation: The operation of this RecordOperation.
        :type: str
        """
        allowed_values = ["REQUIRE", "PROHIBIT", "ADD", "REMOVE"]
        if not value_allowed_none_or_none_sentinel(operation, allowed_values):
            raise ValueError(
                "Invalid value for `operation`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._operation = operation

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
