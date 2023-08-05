# -*- coding: utf-8 -*-

"""
    apimaticcalculatorlatest

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""

from apimaticcalculatorlatest.api_helper import APIHelper
from apimaticcalculatorlatest.configuration import Configuration
from apimaticcalculatorlatest.controllers.base_controller import BaseController
from apimaticcalculatorlatest.http.auth.custom_query_auth import CustomQueryAuth
from apimaticcalculatorlatest.models.rates_availabilityresponse import RatesAvailabilityresponse

class RatesAndAvailabilityController(BaseController):

    """A Controller to access Endpoints in the apimaticcalculatorlatest API."""


    def getratesandavailabilityproduct_id(self,
                                          content_type,
                                          product_id):
        """Does a GET request to /ra/{productId}.

        This function allows logged in users to get rates and availability for
        the specific product.
        Every API call in this section should be with PM credentials.

        Args:
            content_type (string): TODO: type description here. Example: 
            product_id (string): ID of the property

        Returns:
            RatesAvailabilityresponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/ra/{productId}'
        _url_path = APIHelper.append_url_with_template_parameters(_url_path, { 
            'productId': product_id
        })
        _query_builder = Configuration.base_uri
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json',
            'Content-Type': content_type
        }

        # Prepare and execute request
        _request = self.http_client.get(_query_url, headers=_headers)
        CustomQueryAuth.apply(_request)
        _context = self.execute_request(_request)
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, RatesAvailabilityresponse.from_dictionary)

    def createandupdateratesandavailability(self,
                                            content_type,
                                            body):
        """Does a POST request to /ra.

        Create and update calls are the same. When data is sent, if the data
        already exists in BookingPal - that data will be updated. Otherwise it
        will be created (inserted). If you want to update data for some
        period, you should just send data for these dates. All other data (for
        other dates) will remain untouched. This allows you to update only
        changed periods and we will not delete previously sent data for other
        periods.
        In the case of a first data push, all data for one property should be
        sent in one request.  When making updates or changes to existing data,
        then all changed data should be sent in one request.
        Note: if property is set to use LOS rates (supportedLosRates) - only
        field leadTime, array availableCount and availability can be updated
        in this API call (for MLT property). For SGL property only leadTime
        and availability can be updated. This API call can not be used for OWN
        properties.
        Important: Maximum allowed end date in any data type is 3 years in
        future.
        Every API call in this section should be with PM credentials.

        Args:
            content_type (string): TODO: type description here. Example: 
            body (CreateandupdateratesandavailabilityRequest): TODO: type
                description here. Example: 

        Returns:
            RatesAvailabilityresponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/ra'
        _query_builder = Configuration.base_uri
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json',
            'Content-Type': content_type
        }

        # Prepare and execute request
        _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
        CustomQueryAuth.apply(_request)
        _context = self.execute_request(_request)
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, RatesAvailabilityresponse.from_dictionary)
