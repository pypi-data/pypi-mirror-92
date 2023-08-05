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


class ItemData(object):
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
        'name': 'str',
        'sku': 'str',
        'price': 'MoneyWithCurrencyCode',
        'quantity': 'float',
        'description': 'str'
    }

    attribute_map = {
        'name': 'Name',
        'sku': 'Sku',
        'price': 'Price',
        'quantity': 'Quantity',
        'description': 'Description'
    }

    def __init__(self, name=None, sku=None, price=None, quantity=None, description=None):  # noqa: E501
        """ItemData - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._sku = None
        self._price = None
        self._quantity = None
        self._description = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if sku is not None:
            self.sku = sku
        if price is not None:
            self.price = price
        self.quantity = quantity
        if description is not None:
            self.description = description

    @property
    def name(self):
        """Gets the name of this ItemData.  # noqa: E501


        :return: The name of this ItemData.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ItemData.


        :param name: The name of this ItemData.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def sku(self):
        """Gets the sku of this ItemData.  # noqa: E501


        :return: The sku of this ItemData.  # noqa: E501
        :rtype: str
        """
        return self._sku

    @sku.setter
    def sku(self, sku):
        """Sets the sku of this ItemData.


        :param sku: The sku of this ItemData.  # noqa: E501
        :type: str
        """

        self._sku = sku

    @property
    def price(self):
        """Gets the price of this ItemData.  # noqa: E501


        :return: The price of this ItemData.  # noqa: E501
        :rtype: MoneyWithCurrencyCode
        """
        return self._price

    @price.setter
    def price(self, price):
        """Sets the price of this ItemData.


        :param price: The price of this ItemData.  # noqa: E501
        :type: MoneyWithCurrencyCode
        """

        self._price = price

    @property
    def quantity(self):
        """Gets the quantity of this ItemData.  # noqa: E501


        :return: The quantity of this ItemData.  # noqa: E501
        :rtype: float
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this ItemData.


        :param quantity: The quantity of this ItemData.  # noqa: E501
        :type: float
        """
        
        if quantity is None:
            raise ValueError("Invalid value for `quantity`, must not be `None`")  # noqa: E501

        self._quantity = quantity

    @property
    def description(self):
        """Gets the description of this ItemData.  # noqa: E501


        :return: The description of this ItemData.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ItemData.


        :param description: The description of this ItemData.  # noqa: E501
        :type: str
        """

        self._description = description

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
        if issubclass(ItemData, dict):
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
        if not isinstance(other, ItemData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
