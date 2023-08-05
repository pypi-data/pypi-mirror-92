# coding: utf-8

"""
    splitit-web-api-public-sdk

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class GetResourcesRequest(object):
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
        'system_text_categories': 'list[SystemTextCategory]',
        'request_context': 'GetResourcesRequestContext'
    }

    attribute_map = {
        'system_text_categories': 'SystemTextCategories',
        'request_context': 'RequestContext'
    }

    def __init__(self, system_text_categories=None, request_context=None):  # noqa: E501
        """GetResourcesRequest - a model defined in Swagger"""  # noqa: E501

        self._system_text_categories = None
        self._request_context = None
        self.discriminator = None

        if system_text_categories is not None:
            self.system_text_categories = system_text_categories
        if request_context is not None:
            self.request_context = request_context

    @property
    def system_text_categories(self):
        """Gets the system_text_categories of this GetResourcesRequest.  # noqa: E501


        :return: The system_text_categories of this GetResourcesRequest.  # noqa: E501
        :rtype: list[SystemTextCategory]
        """
        return self._system_text_categories

    @system_text_categories.setter
    def system_text_categories(self, system_text_categories):
        """Sets the system_text_categories of this GetResourcesRequest.


        :param system_text_categories: The system_text_categories of this GetResourcesRequest.  # noqa: E501
        :type: list[SystemTextCategory]
        """

        self._system_text_categories = system_text_categories

    @property
    def request_context(self):
        """Gets the request_context of this GetResourcesRequest.  # noqa: E501


        :return: The request_context of this GetResourcesRequest.  # noqa: E501
        :rtype: GetResourcesRequestContext
        """
        return self._request_context

    @request_context.setter
    def request_context(self, request_context):
        """Sets the request_context of this GetResourcesRequest.


        :param request_context: The request_context of this GetResourcesRequest.  # noqa: E501
        :type: GetResourcesRequestContext
        """

        self._request_context = request_context

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
        if issubclass(GetResourcesRequest, dict):
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
        if not isinstance(other, GetResourcesRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
