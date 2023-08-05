# -*- coding: utf-8 -*-

"""
    apimaticcalculatorlatest

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""

from apimaticcalculatorlatest.api_helper import APIHelper


class Configuration(object):

    """A class used for configuring the SDK by a user.

    This class need not be instantiated and all properties and methods
    are accessible without instance creation.

    """

    # Set the array parameter serialization method
    # (allowed: indexed, unindexed, plain, csv, tsv, psv)
    array_serialization = "indexed"

    # The base Uri for API calls
    base_uri = 'https://apidemo.mybookingpal.com'

    # Token which need to be passed in every request as GET parameter. You will
    # get this token in authorization response. Token is valid 1 hour.
    # TODO: Set an appropriate value
    jwt = None

