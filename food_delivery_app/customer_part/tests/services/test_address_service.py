from django.contrib.auth.models import User
from django.core.exceptions import BadRequest
from django.test import TestCase
from faker import Faker  # type: ignore
from unittest.mock import patch, Mock

from ...dtos import MapsResponseResourcesDto
from ...exceptions import Unauthorized, InternalServerError
from ...models import Address
from ...services.address_service import AddressService
from ...services.maps_service import MapsService


class AddressServiceTests(TestCase):
    address_service = AddressService()
    query = "Some Address"
    faker = Faker()

    @patch.object(MapsService, "get_location_by_query")
    def test_get_address_options_returns_list_of_options_successfully(
        self, get_location_by_query_mock
    ):
        """Asserts that the method for fetching address options successfully returns options"""

        fake_address = self.faker.address()
        maps_response_resources_dto = MapsResponseResourcesDto(
            bbox=[float(self.faker.latitude()), float(self.faker.longitude())],
            address_information={
                "formattedAddress": fake_address,
                "addressLine": fake_address,
                "adminDistrict": self.faker.country_code(),
                "adminDistrict2": self.faker.country_code(),
                "countryRegion": self.faker.country(),
                "locality": self.faker.city(),
                "postalCode": self.faker.postcode(),
            },
        )
        get_location_by_query_mock.return_value = [maps_response_resources_dto]
        address_options = self.address_service.get_address_options(self.query)

        self.assertIs(type(address_options), list)
        self.assertIs(type(address_options[0]), dict)

    @patch.object(AddressService, "log_errors")
    @patch.object(MapsService, "get_location_by_query")
    def test_get_address_options_returns_empty_list_when_bad_request_error_raised(
        self, get_location_by_query_mock, log_errors_mock
    ):
        """Asserts that the method for fetching address options returns an empty list if the bad request error is raised"""

        log_errors_mock.return_value = None
        get_location_by_query_mock.side_effect = Exception(BadRequest)

        address_options = self.address_service.get_address_options(self.query)

        self.assertIs(type(address_options), list)
        self.assertEqual(len(address_options), 0)

    @patch.object(AddressService, "log_errors")
    @patch.object(MapsService, "get_location_by_query")
    def test_get_address_options_returns_empty_list_when_unauthorized_error_raised(
        self, get_location_by_query_mock, log_errors_mock
    ):
        """Asserts that the method for fetching address options returns an empty list if the unauthorized error is raised"""

        log_errors_mock.return_value = None
        get_location_by_query_mock.side_effect = Exception(Unauthorized)

        address_options = self.address_service.get_address_options(self.query)

        self.assertIs(type(address_options), list)
        self.assertEqual(len(address_options), 0)

    @patch.object(AddressService, "log_errors")
    @patch.object(MapsService, "get_location_by_query")
    def test_get_address_options_returns_empty_list_when_internal_server_error_raised(
        self, get_location_by_query_mock, log_errors_mock
    ):
        """Asserts that the method for fetching address options returns an empty list if the internal server error is raised"""

        log_errors_mock.return_value = None
        get_location_by_query_mock.side_effect = Exception(InternalServerError)

        address_options = self.address_service.get_address_options(self.query)

        self.assertIs(type(address_options), list)
        self.assertEqual(len(address_options), 0)

    @patch.object(AddressService, "log_errors")
    @patch.object(MapsService, "get_location_by_query")
    def test_get_address_options_returns_empty_list_when_exception_raised(
        self, get_location_by_query_mock, log_errors_mock
    ):
        """Asserts that the method for fetching address options returns an empty list if the general exception is raised"""

        log_errors_mock.return_value = None
        get_location_by_query_mock.side_effect = Exception()

        address_options = self.address_service.get_address_options(self.query)

        self.assertIs(type(address_options), list)
        self.assertEqual(len(address_options), 0)

    @patch.object(AddressService, "get_model_instance")
    def test_create_returns_address_model_instance_when_created_successfully(
        self, get_model_instance_mock
    ):
        """Asserts that the method for creating an address returns an address if it is successfully creation"""

        user = Mock(spec=User)

        address_mock = Mock(spec=Address)
        get_model_instance_mock.return_value = address_mock
        address_mock.full_clean.return_value = None
        address_mock.save.return_value = None

        fake_address = self.faker.address()
        result = self.address_service.create(
            latitude=self.faker.latitude(),
            longitude=self.faker.longitude(),
            raw_address=fake_address,
            address_line=fake_address,
            district_1=self.faker.country_code(),
            district_2=self.faker.country_code(),
            country=self.faker.country(),
            locality=self.faker.city(),
            postal_code=self.faker.postcode(),
            user=user,
        )

        self.assertIsInstance(result, Mock)
