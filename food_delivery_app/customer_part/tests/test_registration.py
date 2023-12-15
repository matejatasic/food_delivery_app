import base64
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import ValidationError
from django.test import TestCase
from django.urls import reverse
import os
from http import HTTPStatus

from food_delivery_app.settings import MEDIA_ROOT
from ..models import Profile


class RegistrationTests(TestCase):
    registration_url: str = reverse("register")
    home_url: str = reverse("home")

    def setUp(self) -> None:
        self.username: str = "user"
        self.image_name: str = "img_avatar"
        self.file_image_name: str = f"{self.image_name}.png"

        image_content: bytes = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAUA"
            + "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
            + "9TXL0Y4OHwAAAABJRU5ErkJggg=="
        )
        image: SimpleUploadedFile = SimpleUploadedFile(
            self.file_image_name, image_content, "image/png"
        )

        self.payload: dict[str, str | SimpleUploadedFile] = {
            "username": self.username,
            "password1": "p@ssword123",
            "password2": "p@ssword123",
            "email": "user@test.com",
            "address": "Some address",
            "image": image,
        }

    def tearDown(self) -> None:
        profile_pictures_folder: str = os.path.join(MEDIA_ROOT, "profile_pictures")
        profile_pictures: list[str] = os.listdir(profile_pictures_folder)

        test_pictures: list[str] = [
            picture for picture in profile_pictures if self.image_name in picture
        ]

        for picture in test_pictures:
            os.remove(os.path.join(profile_pictures_folder, picture))

    def test_access_to_restiger_as_authenticated_user_unsuccessful(self):
        self.client.post(self.registration_url, self.payload)
        response = self.client.get(self.registration_url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["location"], self.home_url)

    def test_on_registration_user_created_successfully(self) -> None:
        response = self.client.post(self.registration_url, self.payload)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["location"], self.home_url)
        self.assertEqual(User.objects.count(), 1)

    def test_on_registration_profile_created_successfully(self) -> None:
        response = self.client.post(self.registration_url, self.payload)

        new_profile: Profile = Profile.objects.get(user__username=self.username)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["location"], self.home_url)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(self.payload["username"], new_profile.user.username)
        self.assertIn(self.file_image_name, new_profile.image.name)

    def test_on_registration_user_is_logged_in_successfully(self) -> None:
        self.client.post(self.registration_url, self.payload)

        self.assertTrue(User.objects.get(username=self.username).is_authenticated)

    def test_registration_with_invalid_input_returning_errors(self) -> None:
        # a username that is longer than allowed max_length
        self.payload[
            "username"
        ] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec euismod fermentum ante, in imperdiet augue sodales eget. Cras ante enim, lacinia sed hendrerit nec, dictum venenatis tellus. Donec tempor, elit quis volutpat porttitor, arcu massa tincidunt quam."

        # a confirmation password that is different from the password
        self.payload["password2"] = "some_other_p@assword"

        response = self.client.post(self.registration_url, self.payload)

        form_errors: dict[str, list[ValidationError]] = response.context[
            "form"
        ].errors.as_data()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(form_errors), 2)
