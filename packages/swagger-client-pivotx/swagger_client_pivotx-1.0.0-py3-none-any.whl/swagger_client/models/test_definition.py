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


class TestDefinition(object):
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
        'models': 'list[ModelIdentity]',
        'dataset': 'DatasetIdentity',
        'name': 'str',
        'description': 'str',
        'properties': 'dict(str, str)'
    }

    attribute_map = {
        'models': 'models',
        'dataset': 'dataset',
        'name': 'name',
        'description': 'description',
        'properties': 'properties'
    }

    def __init__(self, models=None, dataset=None, name=None, description=None, properties=None):  # noqa: E501
        """TestDefinition - a model defined in Swagger"""  # noqa: E501

        self._models = None
        self._dataset = None
        self._name = None
        self._description = None
        self._properties = None
        self.discriminator = None

        self.models = models
        if dataset is not None:
            self.dataset = dataset
        self.name = name
        if description is not None:
            self.description = description
        if properties is not None:
            self.properties = properties

    @property
    def models(self):
        """Gets the models of this TestDefinition.  # noqa: E501

        Information about the models used for this accuracy test.  # noqa: E501

        :return: The models of this TestDefinition.  # noqa: E501
        :rtype: list[ModelIdentity]
        """
        return self._models

    @models.setter
    def models(self, models):
        """Sets the models of this TestDefinition.

        Information about the models used for this accuracy test.  # noqa: E501

        :param models: The models of this TestDefinition.  # noqa: E501
        :type: list[ModelIdentity]
        """
        if models is None:
            raise ValueError("Invalid value for `models`, must not be `None`")  # noqa: E501

        self._models = models

    @property
    def dataset(self):
        """Gets the dataset of this TestDefinition.  # noqa: E501

        Information about the dataset used in the test.  # noqa: E501

        :return: The dataset of this TestDefinition.  # noqa: E501
        :rtype: DatasetIdentity
        """
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        """Sets the dataset of this TestDefinition.

        Information about the dataset used in the test.  # noqa: E501

        :param dataset: The dataset of this TestDefinition.  # noqa: E501
        :type: DatasetIdentity
        """

        self._dataset = dataset

    @property
    def name(self):
        """Gets the name of this TestDefinition.  # noqa: E501

        The name of the object.  # noqa: E501

        :return: The name of this TestDefinition.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this TestDefinition.

        The name of the object.  # noqa: E501

        :param name: The name of this TestDefinition.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this TestDefinition.  # noqa: E501

        The description of the object.  # noqa: E501

        :return: The description of this TestDefinition.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this TestDefinition.

        The description of the object.  # noqa: E501

        :param description: The description of this TestDefinition.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def properties(self):
        """Gets the properties of this TestDefinition.  # noqa: E501

        The custom properties of this entity. The maximum allowed key length is 64 characters, the maximum  allowed value length is 256 characters and the count of allowed entries is 10.  # noqa: E501

        :return: The properties of this TestDefinition.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this TestDefinition.

        The custom properties of this entity. The maximum allowed key length is 64 characters, the maximum  allowed value length is 256 characters and the count of allowed entries is 10.  # noqa: E501

        :param properties: The properties of this TestDefinition.  # noqa: E501
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
        if issubclass(TestDefinition, dict):
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
        if not isinstance(other, TestDefinition):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
