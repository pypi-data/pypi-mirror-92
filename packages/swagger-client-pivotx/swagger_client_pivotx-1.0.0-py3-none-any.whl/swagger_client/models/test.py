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


class Test(object):
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
        'results_url': 'str',
        'id': 'str',
        'word_error_rate': 'float',
        'last_action_date_time': 'datetime',
        'status': 'str',
        'created_date_time': 'datetime',
        'models': 'list[Model]',
        'dataset': 'Dataset',
        'name': 'str',
        'description': 'str',
        'properties': 'dict(str, str)'
    }

    attribute_map = {
        'results_url': 'resultsUrl',
        'id': 'id',
        'word_error_rate': 'wordErrorRate',
        'last_action_date_time': 'lastActionDateTime',
        'status': 'status',
        'created_date_time': 'createdDateTime',
        'models': 'models',
        'dataset': 'dataset',
        'name': 'name',
        'description': 'description',
        'properties': 'properties'
    }

    def __init__(self, results_url=None, id=None, word_error_rate=None, last_action_date_time=None, status=None, created_date_time=None, models=None, dataset=None, name=None, description=None, properties=None):  # noqa: E501
        """Test - a model defined in Swagger"""  # noqa: E501

        self._results_url = None
        self._id = None
        self._word_error_rate = None
        self._last_action_date_time = None
        self._status = None
        self._created_date_time = None
        self._models = None
        self._dataset = None
        self._name = None
        self._description = None
        self._properties = None
        self.discriminator = None

        if results_url is not None:
            self.results_url = results_url
        self.id = id
        if word_error_rate is not None:
            self.word_error_rate = word_error_rate
        if last_action_date_time is not None:
            self.last_action_date_time = last_action_date_time
        if status is not None:
            self.status = status
        if created_date_time is not None:
            self.created_date_time = created_date_time
        self.models = models
        if dataset is not None:
            self.dataset = dataset
        self.name = name
        if description is not None:
            self.description = description
        if properties is not None:
            self.properties = properties

    @property
    def results_url(self):
        """Gets the results_url of this Test.  # noqa: E501

        The URL that can be used to download the test results.  Each line in the file represents a tab separated list of filename, reference transcription and decoder output.                The URL will only be valid, if the test completed successfully.  # noqa: E501

        :return: The results_url of this Test.  # noqa: E501
        :rtype: str
        """
        return self._results_url

    @results_url.setter
    def results_url(self, results_url):
        """Sets the results_url of this Test.

        The URL that can be used to download the test results.  Each line in the file represents a tab separated list of filename, reference transcription and decoder output.                The URL will only be valid, if the test completed successfully.  # noqa: E501

        :param results_url: The results_url of this Test.  # noqa: E501
        :type: str
        """

        self._results_url = results_url

    @property
    def id(self):
        """Gets the id of this Test.  # noqa: E501

        The identifier of this entity.  # noqa: E501

        :return: The id of this Test.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Test.

        The identifier of this entity.  # noqa: E501

        :param id: The id of this Test.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def word_error_rate(self):
        """Gets the word_error_rate of this Test.  # noqa: E501

        The word error rate of the tested model.  # noqa: E501

        :return: The word_error_rate of this Test.  # noqa: E501
        :rtype: float
        """
        return self._word_error_rate

    @word_error_rate.setter
    def word_error_rate(self, word_error_rate):
        """Sets the word_error_rate of this Test.

        The word error rate of the tested model.  # noqa: E501

        :param word_error_rate: The word_error_rate of this Test.  # noqa: E501
        :type: float
        """

        self._word_error_rate = word_error_rate

    @property
    def last_action_date_time(self):
        """Gets the last_action_date_time of this Test.  # noqa: E501

        The time-stamp when the current status was entered.  The time stamp is encoded as ISO 8601 date and time format  (\"YYYY-MM-DDThh:mm:ssZ\", see https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations).  # noqa: E501

        :return: The last_action_date_time of this Test.  # noqa: E501
        :rtype: datetime
        """
        return self._last_action_date_time

    @last_action_date_time.setter
    def last_action_date_time(self, last_action_date_time):
        """Sets the last_action_date_time of this Test.

        The time-stamp when the current status was entered.  The time stamp is encoded as ISO 8601 date and time format  (\"YYYY-MM-DDThh:mm:ssZ\", see https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations).  # noqa: E501

        :param last_action_date_time: The last_action_date_time of this Test.  # noqa: E501
        :type: datetime
        """

        self._last_action_date_time = last_action_date_time

    @property
    def status(self):
        """Gets the status of this Test.  # noqa: E501

        The status of the object.  # noqa: E501

        :return: The status of this Test.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Test.

        The status of the object.  # noqa: E501

        :param status: The status of this Test.  # noqa: E501
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
        """Gets the created_date_time of this Test.  # noqa: E501

        The time-stamp when the object was created.  The time stamp is encoded as ISO 8601 date and time format  (\"YYYY-MM-DDThh:mm:ssZ\", see https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations).  # noqa: E501

        :return: The created_date_time of this Test.  # noqa: E501
        :rtype: datetime
        """
        return self._created_date_time

    @created_date_time.setter
    def created_date_time(self, created_date_time):
        """Sets the created_date_time of this Test.

        The time-stamp when the object was created.  The time stamp is encoded as ISO 8601 date and time format  (\"YYYY-MM-DDThh:mm:ssZ\", see https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations).  # noqa: E501

        :param created_date_time: The created_date_time of this Test.  # noqa: E501
        :type: datetime
        """

        self._created_date_time = created_date_time

    @property
    def models(self):
        """Gets the models of this Test.  # noqa: E501

        Information about the models used for this accuracy test.  # noqa: E501

        :return: The models of this Test.  # noqa: E501
        :rtype: list[Model]
        """
        return self._models

    @models.setter
    def models(self, models):
        """Sets the models of this Test.

        Information about the models used for this accuracy test.  # noqa: E501

        :param models: The models of this Test.  # noqa: E501
        :type: list[Model]
        """
        if models is None:
            raise ValueError("Invalid value for `models`, must not be `None`")  # noqa: E501

        self._models = models

    @property
    def dataset(self):
        """Gets the dataset of this Test.  # noqa: E501

        Information about the dataset used in the test.  # noqa: E501

        :return: The dataset of this Test.  # noqa: E501
        :rtype: Dataset
        """
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        """Sets the dataset of this Test.

        Information about the dataset used in the test.  # noqa: E501

        :param dataset: The dataset of this Test.  # noqa: E501
        :type: Dataset
        """

        self._dataset = dataset

    @property
    def name(self):
        """Gets the name of this Test.  # noqa: E501

        The name of the object.  # noqa: E501

        :return: The name of this Test.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Test.

        The name of the object.  # noqa: E501

        :param name: The name of this Test.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this Test.  # noqa: E501

        The description of the object.  # noqa: E501

        :return: The description of this Test.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Test.

        The description of the object.  # noqa: E501

        :param description: The description of this Test.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def properties(self):
        """Gets the properties of this Test.  # noqa: E501

        The custom properties of this entity. The maximum allowed key length is 64 characters, the maximum  allowed value length is 256 characters and the count of allowed entries is 10.  # noqa: E501

        :return: The properties of this Test.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this Test.

        The custom properties of this entity. The maximum allowed key length is 64 characters, the maximum  allowed value length is 256 characters and the count of allowed entries is 10.  # noqa: E501

        :param properties: The properties of this Test.  # noqa: E501
        :type: dict(str, str)
        """

        self._properties = properties

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
        if issubclass(Test, dict):
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
        if not isinstance(other, Test):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
