# coding: utf-8

"""
    Speech Services API v2.0

    Speech Services API v2.0.  # noqa: E501

    OpenAPI spec version: v2.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class EndpointData(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'data_url': 'str',
        'last_action_date_time': 'datetime',
        'status': 'str',
        'created_date_time': 'datetime',
        'start_date': 'datetime',
        'end_date': 'datetime'
    }

    attribute_map = {
        'id': 'id',
        'data_url': 'dataUrl',
        'last_action_date_time': 'lastActionDateTime',
        'status': 'status',
        'created_date_time': 'createdDateTime',
        'start_date': 'startDate',
        'end_date': 'endDate'
    }

    def __init__(self, id=None, data_url=None, last_action_date_time=None, status=None, created_date_time=None, start_date=None, end_date=None):  # noqa: E501
        """EndpointData - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._data_url = None
        self._last_action_date_time = None
        self._status = None
        self._created_date_time = None
        self._start_date = None
        self._end_date = None
        self.discriminator = None

        self.id = id
        if data_url is not None:
            self.data_url = data_url
        if last_action_date_time is not None:
            self.last_action_date_time = last_action_date_time
        if status is not None:
            self.status = status
        if created_date_time is not None:
            self.created_date_time = created_date_time
        self.start_date = start_date
        self.end_date = end_date

    @property
    def id(self):
        """Gets the id of this EndpointData.  # noqa: E501

        The identifier of this entity.  # noqa: E501

        :return: The id of this EndpointData.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this EndpointData.

        The identifier of this entity.  # noqa: E501

        :param id: The id of this EndpointData.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def data_url(self):
        """Gets the data_url of this EndpointData.  # noqa: E501

        The resulting data Url for the model deployment.  # noqa: E501

        :return: The data_url of this EndpointData.  # noqa: E501
        :rtype: str
        """
        return self._data_url

    @data_url.setter
    def data_url(self, data_url):
        """Sets the data_url of this EndpointData.

        The resulting data Url for the model deployment.  # noqa: E501

        :param data_url: The data_url of this EndpointData.  # noqa: E501
        :type: str
        """

        self._data_url = data_url

    @property
    def last_action_date_time(self):
        """Gets the last_action_date_time of this EndpointData.  # noqa: E501

        The time-stamp when the current status was entered.  The time stamp is encoded as ISO 8601 date and time format  (\"YYYY-MM-DDThh:mm:ssZ\", see https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations).  # noqa: E501

        :return: The last_action_date_time of this EndpointData.  # noqa: E501
        :rtype: datetime
        """
        return self._last_action_date_time

    @last_action_date_time.setter
    def last_action_date_time(self, last_action_date_time):
        """Sets the last_action_date_time of this EndpointData.

        The time-stamp when the current status was entered.  The time stamp is encoded as ISO 8601 date and time format  (\"YYYY-MM-DDThh:mm:ssZ\", see https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations).  # noqa: E501

        :param last_action_date_time: The last_action_date_time of this EndpointData.  # noqa: E501
        :type: datetime
        """

        self._last_action_date_time = last_action_date_time

    @property
    def status(self):
        """Gets the status of this EndpointData.  # noqa: E501

        The status of the object.  # noqa: E501

        :return: The status of this EndpointData.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this EndpointData.

        The status of the object.  # noqa: E501

        :param status: The status of this EndpointData.  # noqa: E501
        :type: str
        """
        allowed_values = ["NotStarted", "Running", "Succeeded", "Failed"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def created_date_time(self):
        """Gets the created_date_time of this EndpointData.  # noqa: E501

        The time-stamp when the object was created.  The time stamp is encoded as ISO 8601 date and time format  (\"YYYY-MM-DDThh:mm:ssZ\", see https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations).  # noqa: E501

        :return: The created_date_time of this EndpointData.  # noqa: E501
        :rtype: datetime
        """
        return self._created_date_time

    @created_date_time.setter
    def created_date_time(self, created_date_time):
        """Sets the created_date_time of this EndpointData.

        The time-stamp when the object was created.  The time stamp is encoded as ISO 8601 date and time format  (\"YYYY-MM-DDThh:mm:ssZ\", see https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations).  # noqa: E501

        :param created_date_time: The created_date_time of this EndpointData.  # noqa: E501
        :type: datetime
        """

        self._created_date_time = created_date_time

    @property
    def start_date(self):
        """Gets the start_date of this EndpointData.  # noqa: E501

        The start date of the demplyment data export.  # noqa: E501

        :return: The start_date of this EndpointData.  # noqa: E501
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this EndpointData.

        The start date of the demplyment data export.  # noqa: E501

        :param start_date: The start_date of this EndpointData.  # noqa: E501
        :type: datetime
        """
        if start_date is None:
            raise ValueError("Invalid value for `start_date`, must not be `None`")  # noqa: E501

        self._start_date = start_date

    @property
    def end_date(self):
        """Gets the end_date of this EndpointData.  # noqa: E501

        The end date of the demplyment data export.  # noqa: E501

        :return: The end_date of this EndpointData.  # noqa: E501
        :rtype: datetime
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """Sets the end_date of this EndpointData.

        The end date of the demplyment data export.  # noqa: E501

        :param end_date: The end_date of this EndpointData.  # noqa: E501
        :type: datetime
        """
        if end_date is None:
            raise ValueError("Invalid value for `end_date`, must not be `None`")  # noqa: E501

        self._end_date = end_date

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(EndpointData, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, EndpointData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
