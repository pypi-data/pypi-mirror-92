# -*- coding: utf-8 -*-

"""
    apimaticcalculatorlatest

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""


class FeeTaxMandatorySetting(object):

    """Implementation of the 'FeeTaxMandatorySetting' model.

    TODO: type model description here.

    Attributes:
        product_id (int): Product id
        is_fee_mandatory (bool): Fee is mandatory
        is_tax_mandatory (bool): Tax is mandatory

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "product_id":'productId',
        "is_fee_mandatory":'isFeeMandatory',
        "is_tax_mandatory":'isTaxMandatory'
    }

    def __init__(self,
                 product_id=None,
                 is_fee_mandatory=None,
                 is_tax_mandatory=None):
        """Constructor for the FeeTaxMandatorySetting class"""

        # Initialize members of the class
        self.product_id = product_id
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
        product_id = dictionary.get('productId')
        is_fee_mandatory = dictionary.get('isFeeMandatory')
        is_tax_mandatory = dictionary.get('isTaxMandatory')

        # Return an object of this model
        return cls(product_id,
                   is_fee_mandatory,
                   is_tax_mandatory)


