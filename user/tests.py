from datetime import timedelta
from unittest import mock

from django.test import TestCase

from functools import partial

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.utils import aware_utcnow

from user.models import User


class TestLoginCase(APITestCase):
    login_url = reverse("user:token_obtain_pair")
    refresh_token_url = reverse("user:token_refresh")
    logout_url = reverse("user:logout")

    email = "test@user.com"
    password = "kah2ie3urh4k"

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(self.email, self.password)
        # self.client.force_authenticate(self.user)

    def _login(self):
        payload = {"email": self.email, "password": self.password}
        r = self.client.post(self.login_url, payload)
        print(r.data)
        body = r.json()
        print(body)
        if "access" in body:
            self.client.credentials(
                HTTP_AUTHORIZATION="Bearer %s" % body["access"]
            )
        return r.status_code, body

    def test_logout_response_200(self):
        _, body = self._login()
        data = {"refresh": body["refresh"]}
        r = self.client.post(self.logout_url, data)
        body = r.content
        print(body)
        self.assertEquals(r.status_code, status.HTTP_200_OK, body)
        self.assertFalse(body, body)

    def test_logout_with_bad_refresh_token_response_400(self):
        self._login()
        data = {"refresh": "dsf.sdfsdf.sdf"}
        r = self.client.post(self.logout_url, data)
        body = r.json()
        self.assertEquals(r.status_code, 400, body)
        self.assertTrue(body, body)

    def test_logout_refresh_token_in_blacklist(self):
        _, body = self._login()
        r = self.client.post(self.logout_url, body)
        token = partial(RefreshToken, body["refresh"])
        self.assertRaises(TokenError, token)

    def test_access_token_still_valid_after_logout(self):
        _, body = self._login()
        self.client.post(self.logout_url, body)
        r = self.client.get(self.profile_url)
        body = r.json()
        self.assertEquals(r.status_code, 200, body)
        self.assertTrue(body, body)

    def test_access_token_invalid_in_hour_after_logout(self):
        _, body = self._login()
        self.client.post(self.logout_url, body)
        m = mock.Mock()
        m.return_value = aware_utcnow() + timedelta(minutes=60)
        with mock.patch("rest_framework_simplejwt.tokens.aware_utcnow", m):
            r = self.client.get(self.profile_url)
            body = r.json()
        self.assertEquals(r.status_code, 401, body)
        self.assertTrue(body, body)
