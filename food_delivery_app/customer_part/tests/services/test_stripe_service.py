from django.core.exceptions import BadRequest
from django.test import TestCase
from stripe import InvalidRequestError
from stripe.checkout import Session
from unittest.mock import patch, Mock

from ..base import faker
from ...services.stripe_service import StripeService


class StripeServiceTests(TestCase):
    stripe_service = StripeService()

    @patch.object(StripeService, "create_session")
    def test_create_checkout_session_returns_client_secret_when_successfully_created_session(
        self, create_session_mock
    ):
        """Asserts that the method for creating the checkout session returns the client secret when it has successfully created the session"""
        session_mock = Mock(Session)
        client_secret = faker.pystr(max_chars=10)
        session_mock.client_secret = client_secret

        create_session_mock.return_value = session_mock
        session_client_secret = self.stripe_service.create_checkout_session(cart={})

        self.assertEqual(client_secret, session_client_secret)

    @patch.object(StripeService, "log_errors")
    @patch.object(StripeService, "create_session")
    def test_create_checkout_session_raises_an_exception_when_invalid_request_exception_raised(
        self, create_session_mock, log_errors_mock
    ):
        """Asserts that the method for creating the checkout session raises an Exception if the InvalidRequestError is raised"""

        log_errors_mock.return_value = None
        create_session_mock.side_effect = Exception(InvalidRequestError)

        self.assertRaises(
            Exception, self.stripe_service.create_checkout_session, {}
        )

    @patch.object(StripeService, "retrieve_session")
    def test_get_session_returns_session_successfully(
        self, retrieve_session_mock
    ):
        """Asserts that the method for getting the session returns the session successfully"""

        session_mock = Mock(Session)
        retrieve_session_mock.return_value = session_mock

        session = self.stripe_service.get_session(session_id="session_id")

        self.assertIsInstance(session, Session)

    def test_get_session_raises_bad_request_when_session_id_not_passed(
        self
    ):
        """Asserts that the method for getting the session raises an BadRequest if the session id is not passed"""

        self.assertRaises(
            BadRequest, self.stripe_service.get_session, None
        )