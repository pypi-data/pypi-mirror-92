# -*- coding: utf-8 -*-

"""
    apimaticcalculatorlatest

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""


class FeeTaxMandatory(object):

    """Implementation of the 'FeeTaxMandatory' model.

    TODO: type model description here.

    Attributes:
        is_fee_mandatory (bool): Used in BookingPal validator. Info does
            property require any fee or not. Default value is TRUE. This setup
            can be overridden on property level with different API call, which
            is stronger.
        is_tax_mandatory (bool): Used in BookingPal validator. Info does
            property require any tax or not. Default value is TRUE. This setup
            can be overridden on property level with different API call, which
            is stronger.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "is_fee_mandatory":'isFeeMandatory',
        "is_tax_mandatory":'isTaxMandatory'
    }

    def __init__(self,
                 is_fee_mandatory=None,
                 is_tax_mandatory=None):
        """Constructor for the FeeTaxMandatory class"""

        # Initialize members of the class
        self.is_fee_mandatory = is_fee_mandatory
        self.is_tax_mandatory = is_tax_mandatory


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
        is_fee_mandatory = dictionary.get('isFeeMandatory')
        is_tax_mandatory = dictionary.get('isTaxMandatory')

        # Return an object of this model
        return cls(is_fee_mandatory,
                   is_tax_mandatory)


