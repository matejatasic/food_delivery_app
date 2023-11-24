import base64
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseRedirect
from django.test import TestCase
from django.urls import reverse
import os
from http import HTTPStatus

from food_delivery_app.settings import MEDIA_ROOT
from .models import Profile


class RegistrationTests(TestCase):
    registration_url: str = reverse("register")
    home_url: str = reverse("home")

    def setUp(self) -> None:
        self.username = "user"
        self.image_name = "img_avatar"
        self.file_image_name = f"{self.image_name}.png"

        image_content = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAUA"
            + "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
            + "9TXL0Y4OHwAAAABJRU5ErkJggg=="
        )
        image = SimpleUploadedFile(self.file_image_name, image_content, "image/png")

        self.payload = {
            "username": self.username,
            "password1": "p@ssword123",
            "password2": "p@ssword123",
            "email": "user@test.com",
            "address": "Some address",
            "image": image,
        }

    def tearDown(self) -> None:
        profile_pictures_folder = os.path.join(MEDIA_ROOT, "profile_pictures")
        profile_pictures = os.listdir(profile_pictures_folder)

        test_pictures = [
            picture for picture in profile_pictures if self.image_name in picture
        ]

        for picture in test_pictures:
            os.remove(os.path.join(profile_pictures_folder, picture))

    def test_on_registration_user_created_successfully(self):
        response: HttpResponseRedirect = self.client.post(
            self.registration_url, self.payload
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["location"], self.home_url)
        self.assertEqual(User.objects.count(), 1)

    def test_on_registration_profile_created_successfully(self):
        response: HttpResponseRedirect = self.client.post(
            self.registration_url, self.payload
        )

        new_profile = Profile.objects.get(user__username=self.username)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["location"], self.home_url)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(self.payload["username"], new_profile.user.username)
        self.assertIn(self.file_image_name, new_profile.image.name)


class LoginTests(TestCase):
    login_url: str = reverse("login")
    registration_url: str = reverse("register")
    home_url: str = reverse("home")

    def setUp(self) -> None:
        self.register_payload = register_payload = {
            "username": "user",
            "password1": "p@ssword123",
            "password2": "p@ssword123",
            "email": "user@test.com",
            "address": "Some address",
        }
        self.login_payload = {
            "username": register_payload["username"],
            "password": register_payload["password1"],
        }

    def test_login_successful_with_valid_user(self):
        self.client.post(self.registration_url, self.register_payload)
        response = self.client.post(self.login_url, self.login_payload)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], self.home_url)
        self.assertTrue(
            User.objects.get(username=self.login_payload["username"]).is_authenticated
        )

    def test_login_with_invalid_input_returns_errors(self):
        response = self.client.post(self.login_url, self.login_payload)

        form_errors = response.context["form"].errors.as_data()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(form_errors), 1)
