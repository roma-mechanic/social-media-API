from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from posts.models import Post, Like, Comments
from posts.serializers import PostListSerializer, PostDetailSerializer
from user_profile.models import UserProfile

POST_URL = reverse("posts:posts-list")


def detail_url(post_id: int):
    return reverse("posts:posts-detail", args=[post_id])


def sample_post(**params):
    defaults = {
        "title": "sample post title",
        "author": "sample author",
        "content": "sample post content",
    }
    defaults.update(params)
    return Post.objects.create(**defaults)


class PostModelTest(TestCase):
    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
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
        user = get_user_model().objects.create_user(
            email="test@email.com", password="password"
        )
        self.author = UserProfile.objects.create(user=user)
        self.post = Post.objects.create(
            title="test title", author=self.author, content="test content"
        )

    def test_get_post_list_auth_optional(self):
        post1 = sample_post(title="title 1", author=self.author)
        post2 = sample_post(title="title 2", author=self.author)
        post3 = sample_post(title="title 3", author=self.author)

        comments = Comments.objects.create(
            author=self.author, post=post3, content="comment"
        )

        content_type_id = ContentType.objects.get_for_model(Post).id
        like = Like.objects.create(
            user=self.author.user,
            object_id=post2.id,
            content_type_id=content_type_id,
        )
        post2.likes.add(like)
        post3.comments.add(comments)

        posts = Post.objects.all()
        res = self.client.get(POST_URL)
        serializer = PostListSerializer(posts, many=True)

        self.assertEqual(res.data, serializer.data)

        serializer1 = PostListSerializer(post1)
        serializer2 = PostListSerializer(post2)
        serializer3 = PostListSerializer(post3)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertIn(serializer3.data, res.data)

    def test_get_post_detail_auth_optional(self):
        url = detail_url(self.post.id)
        res = self.client.get(url)
        posts = Post.objects.all()
        another_user = get_user_model().objects.create_user(
            email="another@email.com", password="anotherpassword"
        )
        is_fan = another_user

        serializer = PostDetailSerializer(
            posts,
            is_fan,
            many=True,
        )
        if serializer.is_valid():
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(serializer.data, res.data)

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


class AuthenticatedPostApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "astronaut@astronaut.com", "password"
        )
        self.client.force_authenticate(self.user)

        self.author = UserProfile.objects.create(user=self.user)
        self.post = Post.objects.create(
            title="test title", author=self.author, content="test content"
        )

    def test_create_post_auth_required(self):
        data = {
            "title": "create title",
            "author": self.author,
            "content": "create content",
        }
        url = reverse("posts:post-create")
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_post_auth_required(self):
        data = {
            "title": "update title",
            "author": self.author,
            "content": "update content",
        }
        url = reverse("posts:post-update", args=[self.post.id])
        res = self.client.patch(url, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_post_auth_required(self):
        url = reverse("posts:post-update", args=[self.post.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
