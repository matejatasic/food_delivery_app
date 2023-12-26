from django.core.exceptions import BadRequest
from django.test import TestCase
from http import HTTPStatus
from unittest.mock import patch, Mock

from ...dtos import MapsResponseResourcesDto
from ...exceptions import Unauthorized, InternalServerError
from ..factories import MapsResponseFactory

from ...services.maps_service import MapsService


class MapsServiceTests(TestCase):
    bing_maps_service = MapsService()
    mock_response: Mock = Mock()
    query = "Some Address"

    @patch.object(MapsService, "send_request")
    def test_get_location_by_query_returns_list_when_response_ok(
        self, send_request_mock
    ) -> None:
        """Asserts that the method for fetching location by query returns a list of MapsResponseResourcesDto-s if the response status code is OK"""

        send_request_mock.return_value = self.mock_response
        self.mock_response.status_code = HTTPStatus.OK
        self.mock_response.json = lambda: MapsResponseFactory()["response"]

        locations = self.bing_maps_service.get_location_by_query(self.query)

        self.assertIs(type(locations), list)
        self.assertIsInstance(locations[0], MapsResponseResourcesDto)

    @patch.object(MapsService, "send_request")
    def test_get_location_by_query_raises_bad_request_error_when_status_code_bad_request(
        self, send_request_mock
    ) -> None:
        """Asserts that the method for fetching location by query raises a BadRequest error if the status code is Bad Request"""

        send_request_mock.return_value = self.mock_response
        self.mock_response.status_code = HTTPStatus.BAD_REQUEST
        self.mock_response.json = lambda: {}

        self.assertRaises(
            BadRequest, self.bing_maps_service.get_location_by_query, self.query
        )

    @patch.object(MapsService, "send_request")
    def test_get_location_by_query_raises_unauthorized_error_when_status_code_unauthorized(
        self, send_request_mock
    ) -> None:
        """Asserts that the method for fetching location by query raises an Unauthorized error if the status code is Unauthorized"""

        send_request_mock.return_value = self.mock_response
        self.mock_response.status_code = HTTPStatus.UNAUTHORIZED

        self.assertRaises(
            Unauthorized, self.bing_maps_service.get_location_by_query, self.query
        )

    @patch.object(MapsService, "send_request")
    def test_get_location_by_query_raises_internal_server_error_when_status_code_internal_server_error(
        self, send_request_mock
    ) -> None:
        """Asserts that the method for fetching location by query raises an InternalServerError error if the status code is Internal Server Error"""

        send_request_mock.return_value = self.mock_response
        self.mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

        self.assertRaises(
            InternalServerError,
            self.bing_maps_service.get_location_by_query,
            self.query,
        )
