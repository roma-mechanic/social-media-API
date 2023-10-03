from django.db.models import Count
from rest_framework import serializers

from posts.models import Post
from user.models import User
from user_profile.models import UserProfile


class UserProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "username",
            "bio",
            "profile_image",
        )


class UserProfileDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(
        source="user.first_name", read_only=True
    )
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    followers = serializers.SlugRelatedField(
        slug_field="email", many=True, read_only=True
    )
    following = serializers.SlugRelatedField(
        slug_field="email", many=True, read_only=True
    )

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user_id",
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "profile_image",
            "followers",
            "following",
        )
        read_only_fields = ("followers", "following")


class UserProfileListSerializer(serializers.ModelSerializer):
    count_posts = serializers.IntegerField(source="get_posts_count")

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user_id",
            "username",
            "count_posts",
            "profile_image",
            "followers",
            "following",
        )

    # def get_count_posts(self, request):
    # user = request.user
    # return Post.objects.select_related("author").filter(author__id=user.id).count()
    # return User.objects.annotate(Count("posts"))
    # return user.posts.count()


class FanSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "full_name",
        )

    def get_full_name(self, obj):
        return obj.get_full_name()
