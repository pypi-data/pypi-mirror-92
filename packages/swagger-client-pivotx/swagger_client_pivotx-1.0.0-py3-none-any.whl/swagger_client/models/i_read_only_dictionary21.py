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


class IReadOnlyDictionary21(object):
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
        '_none': 'list[str]',
        'acoustic': 'list[str]',
        'language': 'list[str]',
        'acoustic_and_language': 'list[str]',
        'sentiment': 'list[str]',
        'diarization': 'list[str]',
        'pronunciation_score': 'list[str]'
    }

    attribute_map = {
        '_none': 'None',
        'acoustic': 'Acoustic',
        'language': 'Language',
        'acoustic_and_language': 'AcousticAndLanguage',
        'sentiment': 'Sentiment',
        'diarization': 'Diarization',
        'pronunciation_score': 'PronunciationScore'
    }

    def __init__(self, _none=None, acoustic=None, language=None, acoustic_and_language=None, sentiment=None, diarization=None, pronunciation_score=None):  # noqa: E501
        """IReadOnlyDictionary21 - a model defined in Swagger"""  # noqa: E501

        self.__none = None
        self._acoustic = None
        self._language = None
        self._acoustic_and_language = None
        self._sentiment = None
        self._diarization = None
        self._pronunciation_score = None
        self.discriminator = None

        if _none is not None:
            self._none = _none
        if acoustic is not None:
            self.acoustic = acoustic
        if language is not None:
            self.language = language
        if acoustic_and_language is not None:
            self.acoustic_and_language = acoustic_and_language
        if sentiment is not None:
            self.sentiment = sentiment
        if diarization is not None:
            self.diarization = diarization
        if pronunciation_score is not None:
            self.pronunciation_score = pronunciation_score

    @property
    def _none(self):
        """Gets the _none of this IReadOnlyDictionary21.  # noqa: E501


        :return: The _none of this IReadOnlyDictionary21.  # noqa: E501
        :rtype: list[str]
        """
        return self.__none

    @_none.setter
    def _none(self, _none):
        """Sets the _none of this IReadOnlyDictionary21.


        :param _none: The _none of this IReadOnlyDictionary21.  # noqa: E501
        :type: list[str]
        """

        self.__none = _none

    @property
    def acoustic(self):
        """Gets the acoustic of this IReadOnlyDictionary21.  # noqa: E501


        :return: The acoustic of this IReadOnlyDictionary21.  # noqa: E501
        :rtype: list[str]
        """
        return self._acoustic

    @acoustic.setter
    def acoustic(self, acoustic):
        """Sets the acoustic of this IReadOnlyDictionary21.


        :param acoustic: The acoustic of this IReadOnlyDictionary21.  # noqa: E501
        :type: list[str]
        """

        self._acoustic = acoustic

    @property
    def language(self):
        """Gets the language of this IReadOnlyDictionary21.  # noqa: E501


        :return: The language of this IReadOnlyDictionary21.  # noqa: E501
        :rtype: list[str]
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this IReadOnlyDictionary21.


        :param language: The language of this IReadOnlyDictionary21.  # noqa: E501
        :type: list[str]
        """

        self._language = language

    @property
    def acoustic_and_language(self):
        """Gets the acoustic_and_language of this IReadOnlyDictionary21.  # noqa: E501


        :return: The acoustic_and_language of this IReadOnlyDictionary21.  # noqa: E501
        :rtype: list[str]
        """
        return self._acoustic_and_language

    @acoustic_and_language.setter
    def acoustic_and_language(self, acoustic_and_language):
        """Sets the acoustic_and_language of this IReadOnlyDictionary21.


        :param acoustic_and_language: The acoustic_and_language of this IReadOnlyDictionary21.  # noqa: E501
        :type: list[str]
        """

        self._acoustic_and_language = acoustic_and_language

    @property
    def sentiment(self):
        """Gets the sentiment of this IReadOnlyDictionary21.  # noqa: E501


        :return: The sentiment of this IReadOnlyDictionary21.  # noqa: E501
        :rtype: list[str]
        """
        return self._sentiment

    @sentiment.setter
    def sentiment(self, sentiment):
        """Sets the sentiment of this IReadOnlyDictionary21.


        :param sentiment: The sentiment of this IReadOnlyDictionary21.  # noqa: E501
        :type: list[str]
        """

        self._sentiment = sentiment

    @property
    def diarization(self):
        """Gets the diarization of this IReadOnlyDictionary21.  # noqa: E501


        :return: The diarization of this IReadOnlyDictionary21.  # noqa: E501
        :rtype: list[str]
        """
        return self._diarization

    @diarization.setter
    def diarization(self, diarization):
        """Sets the diarization of this IReadOnlyDictionary21.


        :param diarization: The diarization of this IReadOnlyDictionary21.  # noqa: E501
        :type: list[str]
        """

        self._diarization = diarization

    @property
    def pronunciation_score(self):
        """Gets the pronunciation_score of this IReadOnlyDictionary21.  # noqa: E501


        :return: The pronunciation_score of this IReadOnlyDictionary21.  # noqa: E501
        :rtype: list[str]
        """
        return self._pronunciation_score

    @pronunciation_score.setter
    def pronunciation_score(self, pronunciation_score):
        """Sets the pronunciation_score of this IReadOnlyDictionary21.


        :param pronunciation_score: The pronunciation_score of this IReadOnlyDictionary21.  # noqa: E501
        :type: list[str]
        """

        self._pronunciation_score = pronunciation_score

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
        if issubclass(IReadOnlyDictionary21, dict):
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
        if not isinstance(other, IReadOnlyDictionary21):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
