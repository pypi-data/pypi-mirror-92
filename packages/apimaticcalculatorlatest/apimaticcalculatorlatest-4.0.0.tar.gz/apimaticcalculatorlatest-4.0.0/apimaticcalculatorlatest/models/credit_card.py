# -*- coding: utf-8 -*-

"""
    apimaticcalculatorlatest

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""

import apimaticcalculatorlatest.models.payment_gateways

class CreditCard(object):

    """Implementation of the 'CreditCard' model.

    TODO: type model description here.

    Attributes:
        credit_card_type (CreditCardTypeEnum): TODO: type description here.
        payment_gateways (PaymentGateways): TODO: type description here.
        credit_card_list (list of CreditCardListEnum): List of acceptable
            credit cards. Allowed only if type is TRANSMIT.
            {MASTER_CARD,VISA,AMERICAN_EXPRESS,DINERS_CLUB,DISCOVER}. If POST
            method selected it will select all creditCardList.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "credit_card_type":'creditCardType',
        "payment_gateways":'paymentGateways',
        "credit_card_list":'creditCardList'
    }

    def __init__(self,
                 credit_card_type=None,
                 payment_gateways=None,
                 credit_card_list=None):
        """Constructor for the CreditCard class"""

        # Initialize members of the class
        self.credit_card_type = credit_card_type
        self.payment_gateways = payment_gateways
        self.credit_card_list = credit_card_list


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
        credit_card_type = dictionary.get('creditCardType')
        payment_gateways = apimaticcalculatorlatest.models.payment_gateways.PaymentGateways.from_dictionary(dictionary.get('paymentGateways')) if dictionary.get('paymentGateways') else None
        credit_card_list = dictionary.get('creditCardList')

        # Return an object of this model
        return cls(credit_card_type,
                   payment_gateways,
                   credit_card_list)


