# -*- coding: utf-8 -*-

"""
    apimaticcalculatorlatest

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""


class ManualPolicies(object):

    """Implementation of the 'ManualPolicies' model.

    TODO: type model description here.

    Attributes:
        charge_value (int): Percentage or flat value which will be charged in
            case of cancellation
        before_days (int): Days before check-in when cancellation policy will
            be charged
        cancellation_fee (float): Cancellation transaction fee - additional
            fee on cancellation

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "charge_value":'chargeValue',
        "before_days":'beforeDays',
        "cancellation_fee":'cancellationFee'
    }

    def __init__(self,
                 charge_value=None,
                 before_days=None,
                 cancellation_fee=None):
        """Constructor for the ManualPolicies class"""

        # Initialize members of the class
        self.charge_value = charge_value
        self.before_days = before_days
        self.cancellation_fee = cancellation_fee


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
        charge_value = dictionary.get('chargeValue')
        before_days = dictionary.get('beforeDays')
        cancellation_fee = dictionary.get('cancellationFee')

        # Return an object of this model
        return cls(charge_value,
                   before_days,
                   cancellation_fee)


