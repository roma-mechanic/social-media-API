from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient, APITestCase

from posts.models import Post, Like, Comments
from user_profile.models import UserProfile

User = get_user_model()

POST_URL = reverse("posts:posts-list")


def detail_url(post_id: int):
    return reverse("posts:posts-detail", args=[post_id])


class PostModelTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(
            email="test@email.com", password="password"
        )
        self.author = UserProfile.objects.create(user=user)

    def test_post_create(self):
        post = Post.objects.create(
            title="post_title",
            author=self.author,
            content="test_content",
        )
        self.assertEqual(post.title, "post_title")
        self.assertEqual(post.author.id, self.author.id)
        self.assertEqual(post.content, "test_content")

    def test_post_like_count_none(self):
        post = Post.objects.create(content="post", author=self.author)
        self.assertEqual(post.total_likes(), 0)

    def test_post_like_count_one(self):
        post = Post.objects.create(content="post", author=self.author)
        content_type_id = ContentType.objects.get_for_model(Post).id
        like = Like.objects.create(
            user=self.author.user,
            object_id=post.id,
            content_type_id=content_type_id,
        )
        post.likes.add(like)
        self.assertEqual(post.total_likes(), 1)


class UnauthenticatedPostApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_user(
            email="test@email.com", password="password"
        )
        author = UserProfile.objects.create(user=user)
        self.post = Post.objects.create(
            title="test title", author=author, content="test content"
        )

    def test_get_post_list_auth_optional(self):
        res = self.client.get(POST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_post_detail_auth_optional(self):
        url = detail_url(self.post.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_post_auth_required(self):
        data = {
            "title": self.post.title,
            "author": self.post.author,
            "content": self.post.content,
        }
        url = reverse("posts:post-create")
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_auth_required(self):
        data = {
            "title": "new title",
            "author": self.post.author,
            "content": "new content",
        }
        url = reverse("posts:post-update", args=[self.post.id])
        res = self.client.patch(url, data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_auth_required(self):
        url = reverse("posts:post-update", args=[self.post.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
