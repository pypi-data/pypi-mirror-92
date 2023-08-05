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


class ScheduleElements(object):
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
        'installment_number': 'int',
        'charge_date': 'datetime',
        'charge_amount': 'float',
        'required_credit': 'float'
    }

    attribute_map = {
        'installment_number': 'InstallmentNumber',
        'charge_date': 'ChargeDate',
        'charge_amount': 'ChargeAmount',
        'required_credit': 'RequiredCredit'
    }

    def __init__(self, installment_number=None, charge_date=None, charge_amount=None, required_credit=None):  # noqa: E501
        """ScheduleElements - a model defined in Swagger"""  # noqa: E501

        self._installment_number = None
        self._charge_date = None
        self._charge_amount = None
        self._required_credit = None
        self.discriminator = None

        self.installment_number = installment_number
        self.charge_date = charge_date
        self.charge_amount = charge_amount
        self.required_credit = required_credit

    @property
    def installment_number(self):
        """Gets the installment_number of this ScheduleElements.  # noqa: E501


        :return: The installment_number of this ScheduleElements.  # noqa: E501
        :rtype: int
        """
        return self._installment_number

    @installment_number.setter
    def installment_number(self, installment_number):
        """Sets the installment_number of this ScheduleElements.


        :param installment_number: The installment_number of this ScheduleElements.  # noqa: E501
        :type: int
        """
        
        if installment_number is None:
            raise ValueError("Invalid value for `installment_number`, must not be `None`")  # noqa: E501

        self._installment_number = installment_number

    @property
    def charge_date(self):
        """Gets the charge_date of this ScheduleElements.  # noqa: E501


        :return: The charge_date of this ScheduleElements.  # noqa: E501
        :rtype: datetime
        """
        return self._charge_date

    @charge_date.setter
    def charge_date(self, charge_date):
        """Sets the charge_date of this ScheduleElements.


        :param charge_date: The charge_date of this ScheduleElements.  # noqa: E501
        :type: datetime
        """
        
        if charge_date is None:
            raise ValueError("Invalid value for `charge_date`, must not be `None`")  # noqa: E501

        self._charge_date = charge_date

    @property
    def charge_amount(self):
        """Gets the charge_amount of this ScheduleElements.  # noqa: E501


        :return: The charge_amount of this ScheduleElements.  # noqa: E501
        :rtype: float
        """
        return self._charge_amount

    @charge_amount.setter
    def charge_amount(self, charge_amount):
        """Sets the charge_amount of this ScheduleElements.


        :param charge_amount: The charge_amount of this ScheduleElements.  # noqa: E501
        :type: float
        """
        
        if charge_amount is None:
            raise ValueError("Invalid value for `charge_amount`, must not be `None`")  # noqa: E501

        self._charge_amount = charge_amount

    @property
    def required_credit(self):
        """Gets the required_credit of this ScheduleElements.  # noqa: E501


        :return: The required_credit of this ScheduleElements.  # noqa: E501
        :rtype: float
        """
        return self._required_credit

    @required_credit.setter
    def required_credit(self, required_credit):
        """Sets the required_credit of this ScheduleElements.


        :param required_credit: The required_credit of this ScheduleElements.  # noqa: E501
        :type: float
        """
        
        if required_credit is None:
            raise ValueError("Invalid value for `required_credit`, must not be `None`")  # noqa: E501

        self._required_credit = required_credit

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
        if issubclass(ScheduleElements, dict):
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
        if not isinstance(other, ScheduleElements):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
