# -*- coding: utf-8 -*-

"""
    apimaticcalculatorlatest

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""


class Location(object):

    """Implementation of the 'Location' model.

    TODO: type model description here.

    Attributes:
        postal_code (string): Postal code of property (Zip code)
        country (string): Country of property. Require 2 letter ISO code
        region (string): State (Region) of PM. Required for US properties.
        city (string): City of property
        street (string): Street of property
        zip_code_9 (string): Set only for US properties (format should be
            zip5-xxxx)

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "postal_code":'postalCode',
        "country":'country',
        "region":'region',
        "city":'city',
        "street":'street',
        "zip_code_9":'zipCode9'
    }

    def __init__(self,
                 postal_code=None,
                 country=None,
                 region=None,
                 city=None,
                 street=None,
                 zip_code_9=None):
        """Constructor for the Location class"""

        # Initialize members of the class
        self.postal_code = postal_code
        self.country = country
        self.region = region
        self.city = city
        self.street = street
        self.zip_code_9 = zip_code_9


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
        postal_code = dictionary.get('postalCode')
        country = dictionary.get('country')
        region = dictionary.get('region')
        city = dictionary.get('city')
        street = dictionary.get('street')
        zip_code_9 = dictionary.get('zipCode9')

        # Return an object of this model
        return cls(postal_code,
                   country,
                   region,
                   city,
                   street,
                   zip_code_9)


