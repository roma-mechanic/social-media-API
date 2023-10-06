from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Post, Like
from user_profile.models import UserProfile

User = get_user_model()


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
