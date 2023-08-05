# -*- coding: utf-8 -*-

"""
    apimaticcalculatorlatest

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""

import apimaticcalculatorlatest.models.description_text_model

class Notes(object):

    """Implementation of the 'Notes' model.

    Model where you can define different kinds of text values. If you need to
    delete some kind of texts, for example short description, you can do this
    on Update call (PUT), and you need to pass empty array for texts value,
    for example :  "shortDescription": {  "texts": [  ] }

    Attributes:
        description (DescriptionTextModel): Model for any kind of description
            text in Property object
        house_rules (DescriptionTextModel): Model for any kind of description
            text in Property object
        fine_print (DescriptionTextModel): Model for any kind of description
            text in Property object
        short_description (DescriptionTextModel): Model for any kind of
            description text in Property object
        name (DescriptionTextModel): Model for any kind of description text in
            Property object

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "description":'description',
        "house_rules":'houseRules',
        "fine_print":'finePrint',
        "short_description":'shortDescription',
        "name":'name'
    }

    def __init__(self,
                 description=None,
                 house_rules=None,
                 fine_print=None,
                 short_description=None,
                 name=None):
        """Constructor for the Notes class"""

        # Initialize members of the class
        self.description = description
        self.house_rules = house_rules
        self.fine_print = fine_print
        self.short_description = short_description
        self.name = name


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
        description = apimaticcalculatorlatest.models.description_text_model.DescriptionTextModel.from_dictionary(dictionary.get('description')) if dictionary.get('description') else None
        house_rules = apimaticcalculatorlatest.models.description_text_model.DescriptionTextModel.from_dictionary(dictionary.get('houseRules')) if dictionary.get('houseRules') else None
        fine_print = apimaticcalculatorlatest.models.description_text_model.DescriptionTextModel.from_dictionary(dictionary.get('finePrint')) if dictionary.get('finePrint') else None
        short_description = apimaticcalculatorlatest.models.description_text_model.DescriptionTextModel.from_dictionary(dictionary.get('shortDescription')) if dictionary.get('shortDescription') else None
        name = apimaticcalculatorlatest.models.description_text_model.DescriptionTextModel.from_dictionary(dictionary.get('name')) if dictionary.get('name') else None

        # Return an object of this model
        return cls(description,
                   house_rules,
                   fine_print,
                   short_description,
                   name)


