from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from user_profile.models import UserProfile
from user_profile.serializers import (
    UserProfileListSerializer,
    UserProfileDetailSerializer,
)


def sample_profile(**params):
    defaults = {"user": "sample user", "username": "sample username"}
    defaults.update(params)
    return UserProfile.objects.create(**defaults)


class UnauthenticatedUserProfileAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "sample@user.com", "password"
        )
        self.another_user = get_user_model().objects.create_user(
            email="another@user.com", password="anotherpass"
        )

    def test_create_profile_auth_required(self):
        payload = {"user": self.user, "username": "test userrname"}
        url = reverse("user_profile:userprofile-create")
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_list_auth_required(self):
        sample_profile(user=self.user, username="username")
        sample_profile(user=self.another_user, username="another username")
        url = reverse("user_profile:userprofile-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail(self):
        profile = sample_profile(user=self.user, username="old username")
        url = reverse("user_profile:userprofile-detail", args=[profile.id])
        res = self.client.get(url)
        profiles = UserProfile.objects.get(user=self.user)
        serializer = UserProfileDetailSerializer(profiles)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile_auth_required(self):
        profile = sample_profile(user=self.user, username="old username")
        url = reverse("user_profile:userprofile-update", args=[profile.id])
        payload = {"username": "new username"}
        res = self.client.patch(url, payload)
        profiles = UserProfile.objects.get(user=self.user)
        serializer = UserProfileDetailSerializer(profiles)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_profile_auth_required(self):
        profile = sample_profile(user=self.user, username="old username")
        url = reverse("user_profile:userprofile-update", args=[profile.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserProfileAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "sample@user.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.another_user = get_user_model().objects.create_user(
            email="another@user.com", password="anotherpass"
        )

    def test_create_profile_auth_required(self):
        payload = {"user": self.user, "username": "test userrname"}
        url = reverse("user_profile:userprofile-create")
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get_profile_list_auth_required(self):
        sample_profile(user=self.user, username="username")
        sample_profile(user=self.another_user, username="another username")
        url = reverse("user_profile:userprofile-list")
        res = self.client.get(url)
        profiles = UserProfile.objects.all()
        serializer = UserProfileListSerializer(profiles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_add_to_profile_followers(self):
        self.client.force_authenticate(self.another_user)
        profile1 = sample_profile(user=self.user, username="username")
        profile2 = sample_profile(
            user=self.another_user, username="another username"
        )
        url = reverse(
            "user_profile:follower-add",
            args=[self.user.id],
        )
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)

        url_detail_user = reverse(
            "user_profile:userprofile-detail", args={profile1.id}
        )
        url_detail_another_user = reverse(
            "user_profile:userprofile-detail", args={profile2.id}
        )
        res_detail_user = self.client.get(url_detail_user)
        res_detail_another_user = self.client.get(url_detail_another_user)

        res_all_profile = self.client.get(
            reverse("user_profile:userprofile-list")
        )

        profiles = UserProfile.objects.all()
        serializer = UserProfileListSerializer(profiles, many=True)

        self.assertEqual(serializer.data, res_all_profile.data)
        self.assertIn(
            self.another_user.email,
            res_detail_user.data["followers"],
        )
        self.assertNotIn(
            self.another_user.email,
            res_detail_user.data["following"],
        )
        self.assertIn(
            self.user.email, res_detail_another_user.data["following"]
        )
        self.assertNotIn(
            self.user.email, res_detail_another_user.data["followers"]
        )

    def test_remove_followers(self):
        self.client.force_authenticate(self.another_user)
        profile1 = sample_profile(user=self.user, username="username")
        profile2 = sample_profile(
            user=self.another_user, username="another username"
        )
        profile1.followers.add(self.another_user)
        profile2.following.add(self.user)

        res = self.client.post(
            reverse("user_profile:-follower-remove", args=[self.user.id])
        )
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)

        url_detail_user = reverse(
            "user_profile:userprofile-detail", args={profile1.id}
        )
        url_detail_another_user = reverse(
            "user_profile:userprofile-detail", args={profile2.id}
        )
        res_detail_user = self.client.get(url_detail_user)
        res_detail_another_user = self.client.get(url_detail_another_user)

        res_all_profile = self.client.get(
            reverse("user_profile:userprofile-list")
        )
        profiles = UserProfile.objects.all()
        serializer = UserProfileListSerializer(profiles, many=True)

        self.assertEqual(serializer.data, res_all_profile.data)
        self.assertNotIn(
            self.another_user.email,
            res_detail_user.data["followers"],
        )
        self.assertNotIn(
            self.another_user.email,
            res_detail_user.data["following"],
        )
        self.assertNotIn(
            self.user.email, res_detail_another_user.data["following"]
        )
        self.assertNotIn(
            self.user.email, res_detail_another_user.data["followers"]
        )

    def test_profile_detail(self):
        profile = sample_profile(user=self.user, username="old username")
        url = reverse("user_profile:userprofile-detail", args=[profile.id])
        res = self.client.get(url)
        profiles = UserProfile.objects.get(user=self.user)
        serializer = UserProfileDetailSerializer(profiles)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_update_profile_auth_required(self):
        profile = sample_profile(user=self.user, username="old username")
        url = reverse("user_profile:userprofile-update", args=[profile.id])
        payload = {"username": "new username"}
        res = self.client.patch(url, payload)
        profiles = UserProfile.objects.get(user=self.user)
        serializer = UserProfileDetailSerializer(profiles)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_delete_profile_auth_required(self):
        profile = sample_profile(user=self.user, username="old username")
        url = reverse("user_profile:userprofile-update", args=[profile.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
