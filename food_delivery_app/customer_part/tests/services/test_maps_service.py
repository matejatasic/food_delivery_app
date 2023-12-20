from django.core.exceptions import BadRequest
from django.test import TestCase
from faker import Faker  # type: ignore
from http import HTTPStatus
from json import dumps
from typing import Any
from unittest.mock import patch

from ...dtos import MapsResponseResourcesDto
from ...exceptions import Unauthorized, InternalServerError
from ...services.maps_service import MapsService


class MockResponse:
    def __init__(self) -> None:
        pass

    def initialize(
        self, data: dict[str, Any] | list[Any], status_code: int = HTTPStatus.OK
    ):
        self.__data = data
        self.__status_code = status_code

    def json(self, should_convert_to_json=False) -> str | dict[str, Any] | list[Any]:
        """Returns the json-encoded content of data if specified, otherwise data in its original type"""

        return self.__data if not should_convert_to_json else dumps(self.__data)

    @property
    def status_code(self) -> int:
        return self.__status_code

    @property
    def headers(self) -> str:
        """A headers sample from Bing Maps Rest Services response"""

        return dumps(
            {
                "Cache-Control": "no-cache",
                "Transfer-Encoding": "chunked",
                "Content-Type": "application/json; charset=utf-8",
                "Server": "Microsoft-IIS/10.0",
                "X-BM-TraceID": "54a5b8981fc146a9b920a11ca5496bc6",
                "X-BM-FE-Elapsed": "3",
                "X-BM-Srv": "DU00003070",
                "X-MS-BM-WS-INFO": "0",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,X-FD-Features,X-FD-FLIGHT,PreferAnonymous",
                "X-AspNet-Version": "4.0.30319",
                "X-Powered-By": "ASP.NET",
                "Date": "Wed, 29 Nov 2023 16:29:20 GMT",
            }
        )


class MapsServiceTests(TestCase):
    bing_maps_service = MapsService()
    mock_response = MockResponse()
    query = "Some Address"
    faker = Faker()

    @patch.object(MapsService, "send_request")
    def test_get_location_by_query_returns_list_when_response_ok(
        self, send_request_mock
    ) -> None:
        """Asserts that the method for fetching location by query returns a list of MapsResponseResourcesDto-s if the response status code is OK"""

        send_request_mock.return_value = self.mock_response
        fake_address = self.faker.address()
        data = {
            "resourceSets": [
                {
                    "resources": [
                        {
                            "bbox": [
                                float(self.faker.latitude()),
                                float(self.faker.longitude()),
                            ],
                            "address": {
                                "formattedAddress": fake_address,
                                "addressLine": fake_address,
                                "adminDistrict": self.faker.country_code(),
                                "adminDistrict2": self.faker.country_code(),
                                "countryRegion": self.faker.country(),
                                "locality": self.faker.city(),
                                "postalCode": self.faker.postcode(),
                            },
                        }
                    ]
                }
            ]
        }
        self.mock_response.initialize(data)
        locations = self.bing_maps_service.get_location_by_query(self.query)

        self.assertIs(type(locations), list)
        self.assertIsInstance(locations[0], MapsResponseResourcesDto)

    @patch.object(MapsService, "send_request")
    def test_get_location_by_query_raises_bad_request_error_when_status_code_bad_request(
        self, send_request_mock
    ) -> None:
        """Asserts that the method for fetching location by query raises a BadRequest error if the status code is Bad Request"""

        send_request_mock.return_value = self.mock_response
        self.mock_response.initialize({}, HTTPStatus.BAD_REQUEST)

        self.assertRaises(
            BadRequest, self.bing_maps_service.get_location_by_query, self.query
        )

    @patch.object(MapsService, "send_request")
    def test_get_location_by_query_raises_unauthorized_error_when_status_code_unauthorized(
        self, send_request_mock
    ) -> None:
        """Asserts that the method for fetching location by query raises an Unauthorized error if the status code is Unauthorized"""

        send_request_mock.return_value = self.mock_response
        self.mock_response.initialize({}, HTTPStatus.UNAUTHORIZED)

        self.assertRaises(
            Unauthorized, self.bing_maps_service.get_location_by_query, self.query
        )

    @patch.object(MapsService, "send_request")
    def test_get_location_by_query_raises_internal_server_error_when_status_code_internal_server_error(
        self, send_request_mock
    ) -> None:
        """Asserts that the method for fetching location by query raises an InternalServerError error if the status code is Internal Server Error"""

        send_request_mock.return_value = self.mock_response
        self.mock_response.initialize({}, HTTPStatus.INTERNAL_SERVER_ERROR)

        self.assertRaises(
            InternalServerError,
            self.bing_maps_service.get_location_by_query,
            self.query,
        )
