# -*- coding: utf-8 -*-

"""
    apimaticcalculatorlatest

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""


class CheckIn(object):

    """Implementation of the 'CheckIn' model.

    TODO: type model description here.

    Attributes:
        monday (bool): Determines if check in could be made on monday
        tuesday (bool): Determines if check in could be made on tuesday
        wednesday (bool): Determines if check in could be made on wednesday
        thursday (bool): Determines if check in could be made on thursday
        friday (bool): Determines if check in could be made on friday
        saturday (bool): Determines if check in could be made on saturday
        sunday (bool): Determines if check in could be made on sunday

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "monday":'monday',
        "tuesday":'tuesday',
        "wednesday":'wednesday',
        "thursday":'thursday',
        "friday":'friday',
        "saturday":'saturday',
        "sunday":'sunday'
    }

    def __init__(self,
                 monday=None,
                 tuesday=None,
                 wednesday=None,
                 thursday=None,
                 friday=None,
                 saturday=None,
                 sunday=None):
        """Constructor for the CheckIn class"""

        # Initialize members of the class
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.sunday = sunday


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
        monday = dictionary.get('monday')
        tuesday = dictionary.get('tuesday')
        wednesday = dictionary.get('wednesday')
        thursday = dictionary.get('thursday')
        friday = dictionary.get('friday')
        saturday = dictionary.get('saturday')
        sunday = dictionary.get('sunday')

        # Return an object of this model
        return cls(monday,
                   tuesday,
                   wednesday,
                   thursday,
                   friday,
                   saturday,
                   sunday)


