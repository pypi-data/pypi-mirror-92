# -*- coding: utf-8 -*-

"""
    apimaticcalculatorlatest

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""

import dateutil.parser

class Yield(object):

    """Implementation of the 'Yield' model.

    TODO: type model description here.

    Attributes:
        begin_date (date): From date. Date should be in format "yyyy-MM-dd"
        end_date (date): To date. Date should be in format "yyyy-MM-dd"
        amount (float): Yield amount
        modifier (YieldmodifierEnum): TODO: type description here.
        weekend_param (WeekendParamEnum): TODO: type description here.
        param (int): Parameter. It can verify depending on what YMR was set.
            More details about params you can see in the description above.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "begin_date":'beginDate',
        "end_date":'endDate',
        "amount":'amount',
        "modifier":'modifier',
        "weekend_param":'weekendParam',
        "param":'param'
    }

    def __init__(self,
                 begin_date=None,
                 end_date=None,
                 amount=None,
                 modifier=None,
                 weekend_param=None,
                 param=None):
        """Constructor for the Yield class"""

        # Initialize members of the class
        self.begin_date = begin_date
        self.end_date = end_date
        self.amount = amount
        self.modifier = modifier
        self.weekend_param = weekend_param
        self.param = param


    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        begin_date = dateutil.parser.parse(dictionary.get('beginDate')).date() if dictionary.get('beginDate') else None
        end_date = dateutil.parser.parse(dictionary.get('endDate')).date() if dictionary.get('endDate') else None
        amount = dictionary.get('amount')
        modifier = dictionary.get('modifier')
        weekend_param = dictionary.get('weekendParam')
        param = dictionary.get('param')

        # Return an object of this model
        return cls(begin_date,
                   end_date,
                   amount,
                   modifier,
                   weekend_param,
                   param)


