from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from posts.models import Comments, Post, Like
from posts.serializers import CommentSerializer, CommentDetailSerializer
from user_profile.models import UserProfile
from rest_framework.test import APIClient, APITestCase


def sample_comment(**params):
    defaults = {
        "author": "sample author",
        "post": "sample post",
        "content": "sample content",
    }
    defaults.update(params)
    return Comments.objects.create(**defaults)


class CommentsModelTest(TestCase):
    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            email="test@email.com", password="password"
        )
        self.author = UserProfile.objects.create(user=user)
        self.post = Post.objects.create(title="test_title", author=self.author)

    def test_comment_create(self):
        comment = sample_comment(
            author=self.author,
            post=self.post,
            content="test_content",
        )
        self.assertEqual(comment.author.id, self.author.id)
        self.assertEqual(comment.content, "test_content")
        self.assertEqual(comment.post.id, self.post.id)

    def test_post_like_count_none(self):
        comment = sample_comment(post=self.post, author=self.author)
        self.assertEqual(comment.total_likes(), 0)

    def test_post_like_count_one(self):
        comment = sample_comment(post=self.post, author=self.author)
        content_type_id = ContentType.objects.get_for_model(Comments).id
        like = Like.objects.create(
            user=self.author.user,
            object_id=comment.id,
            content_type_id=content_type_id,
        )
        comment.likes.add(like)
        self.assertEqual(comment.total_likes(), 1)


class UnauthenticatedCommentApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user = get_user_model().objects.create_user(
            email="test@email.com", password="password"
        )
        self.author = UserProfile.objects.create(
            user=user, username="test username"
        )
        self.post = Post.objects.create(
            title="test title", author=self.author, content="test content"
        )

    def test_get_comments_list_auth_optional(self):
        comment1 = sample_comment(author=self.author, post=self.post)
        comment2 = sample_comment(author=self.author, post=self.post)
        comment3 = sample_comment(author=self.author, post=self.post)

        content_type_id = ContentType.objects.get_for_model(Comments).id
        like = Like.objects.create(
            user=self.author.user,
            object_id=comment3.id,
            content_type_id=content_type_id,
        )
        comment3.likes.add(like)
        res = self.client.get(
            reverse(
                "posts:post-comments-list", kwargs={"post_pk": self.post.id}
            )
        )
        comments = Comments.objects.all()
        serializer = CommentSerializer(comments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

        serializer1 = CommentSerializer(comment1)
        serializer2 = CommentSerializer(comment2)
        serializer3 = CommentSerializer(comment3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertIn(serializer3.data, res.data)

    def test_comment_list_filter_by_author(self):
        user1 = get_user_model().objects.create_user(
            email="Petro@email.com", password="petropassword"
        )
        user2 = get_user_model().objects.create_user(
            email="Roman@mail.com", password="romanpassword"
        )

        author1 = UserProfile.objects.create(
            user=user1, username="petro_username"
        )
        author2 = UserProfile.objects.create(
            user=user2, username="roman_username"
        )
        post = Post.objects.create(title="any title", author=self.author)

        comment1 = sample_comment(author=author1, post=post)
        comment2 = sample_comment(author=author2, post=post)

        serializer1 = CommentSerializer(comment1)
        serializer2 = CommentSerializer(comment2)

        res = self.client.get(
            reverse("posts:post-comments-list", kwargs={"post_pk": post.id}),
            data={"author": "roman"},
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)

    def test_get_detail_comment_auth_optional(self):
        comment = sample_comment(author=self.author, post=self.post)
        another_user = get_user_model().objects.create_user(
            email="another@email.com", password="anotherpassword"
        )
        is_fan = another_user
        url = reverse(
            "posts:post-comments-detail",
            kwargs={"post_pk": self.post.id, "pk": comment.id},
        )
        res = self.client.get(url)
        comments = Comments.objects.all()
        serializer = CommentDetailSerializer(comments, is_fan, many=True)

        if serializer.is_valid():
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(serializer.data, res.data)

    def test_create_comment_auth_required(self):
        data = {
            "author": self.author,
            "post": self.post,
            "content": "test content",
        }
        url = reverse("posts:comment-create", args=[self.post.id])
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_auth_required(self):
        old_comment = sample_comment(
            author=self.author, post=self.post, content="old content"
        )
        data = {
            "author": self.author,
            "post": self.post,
            "content": "new content",
        }
        url = reverse(
            "posts:comment-update", args=[self.post.id, old_comment.id]
        )
        res = self.client.patch(url, data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_auth_required(self):
        old_comment = sample_comment(
            author=self.author, post=self.post, content="old content"
        )
        url = reverse(
            "posts:comment-update", args=[self.post.id, old_comment.id]
        )
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCommentsApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user = get_user_model().objects.create_user(
            email="test@email.com", password="password"
        )
        self.client.force_authenticate(user)
        self.author = UserProfile.objects.create(
            user=user, username="test username"
        )
        self.post = Post.objects.create(
            title="test title", author=self.author, content="test content"
        )

    def test_create_comment_auth_required(self):
        data = {
            "author": self.author,
            "post": self.post,
            "content": "test content",
        }
        url = reverse("posts:comment-create", args=[self.post.id])
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_post_auth_required(self):
        old_comment = sample_comment(
            author=self.author, post=self.post, content="old content"
        )
        data = {
            "author": self.author,
            "post": self.post,
            "content": "new content",
        }
        url = reverse(
            "posts:comment-update", args=[self.post.id, old_comment.id]
        )
        res = self.client.patch(url, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_post_auth_required(self):
        old_comment = sample_comment(
            author=self.author, post=self.post, content="old content"
        )
        url = reverse(
            "posts:comment-update", args=[self.post.id, old_comment.id]
        )
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
