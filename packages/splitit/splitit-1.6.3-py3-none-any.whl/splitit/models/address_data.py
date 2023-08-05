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


class AddressData(object):
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
        'address_line': 'str',
        'address_line2': 'str',
        'city': 'str',
        'country': 'str',
        'state': 'str',
        'zip': 'str',
        'full_address_line': 'str'
    }

    attribute_map = {
        'address_line': 'AddressLine',
        'address_line2': 'AddressLine2',
        'city': 'City',
        'country': 'Country',
        'state': 'State',
        'zip': 'Zip',
        'full_address_line': 'FullAddressLine'
    }

    def __init__(self, address_line=None, address_line2=None, city=None, country=None, state=None, zip=None, full_address_line=None):  # noqa: E501
        """AddressData - a model defined in Swagger"""  # noqa: E501

        self._address_line = None
        self._address_line2 = None
        self._city = None
        self._country = None
        self._state = None
        self._zip = None
        self._full_address_line = None
        self.discriminator = None

        if address_line is not None:
            self.address_line = address_line
        if address_line2 is not None:
            self.address_line2 = address_line2
        if city is not None:
            self.city = city
        if country is not None:
            self.country = country
        if state is not None:
            self.state = state
        if zip is not None:
            self.zip = zip
        if full_address_line is not None:
            self.full_address_line = full_address_line

    @property
    def address_line(self):
        """Gets the address_line of this AddressData.  # noqa: E501


        :return: The address_line of this AddressData.  # noqa: E501
        :rtype: str
        """
        return self._address_line

    @address_line.setter
    def address_line(self, address_line):
        """Sets the address_line of this AddressData.


        :param address_line: The address_line of this AddressData.  # noqa: E501
        :type: str
        """

        self._address_line = address_line

    @property
    def address_line2(self):
        """Gets the address_line2 of this AddressData.  # noqa: E501


        :return: The address_line2 of this AddressData.  # noqa: E501
        :rtype: str
        """
        return self._address_line2

    @address_line2.setter
    def address_line2(self, address_line2):
        """Sets the address_line2 of this AddressData.


        :param address_line2: The address_line2 of this AddressData.  # noqa: E501
        :type: str
        """

        self._address_line2 = address_line2

    @property
    def city(self):
        """Gets the city of this AddressData.  # noqa: E501


        :return: The city of this AddressData.  # noqa: E501
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """Sets the city of this AddressData.


        :param city: The city of this AddressData.  # noqa: E501
        :type: str
        """

        self._city = city

    @property
    def country(self):
        """Gets the country of this AddressData.  # noqa: E501


        :return: The country of this AddressData.  # noqa: E501
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this AddressData.


        :param country: The country of this AddressData.  # noqa: E501
        :type: str
        """

        self._country = country

    @property
    def state(self):
        """Gets the state of this AddressData.  # noqa: E501


        :return: The state of this AddressData.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this AddressData.


        :param state: The state of this AddressData.  # noqa: E501
        :type: str
        """

        self._state = state

    @property
    def zip(self):
        """Gets the zip of this AddressData.  # noqa: E501


        :return: The zip of this AddressData.  # noqa: E501
        :rtype: str
        """
        return self._zip

    @zip.setter
    def zip(self, zip):
        """Sets the zip of this AddressData.


        :param zip: The zip of this AddressData.  # noqa: E501
        :type: str
        """

        self._zip = zip

    @property
    def full_address_line(self):
        """Gets the full_address_line of this AddressData.  # noqa: E501


        :return: The full_address_line of this AddressData.  # noqa: E501
        :rtype: str
        """
        return self._full_address_line

    @full_address_line.setter
    def full_address_line(self, full_address_line):
        """Sets the full_address_line of this AddressData.


        :param full_address_line: The full_address_line of this AddressData.  # noqa: E501
        :type: str
        """

        self._full_address_line = full_address_line

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
        if issubclass(AddressData, dict):
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
        if not isinstance(other, AddressData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
