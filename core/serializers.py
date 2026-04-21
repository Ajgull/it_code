from rest_framework import serializers

from core.models import (
    Category,
    Comment,
    GlobalStopWord,
    Post,
    PostStopWord,
    Tag,
    User,
    Vote,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "avatar", "is_active"]
        read_only_fields = ["id", "is_active"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]
        read_only_fields = ["id"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "description",
            "status",
            "category",
            "tags",
            "author",
            "image",
        ]
        read_only_fields = [
            "id",
            "author",
            "deleted",
            "score",
            "is_hidden_by_score",
            "image",
        ]


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["image"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "author",
            "post_id",
            "tags",
            "parent_comment_id",
            "depth_level",
        ]
        read_only_fields = ["id", "author", "depth_level"]


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "user", "post", "comment", "vote_type"]
        read_only_fields = ["id"]


class GlobalStopWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalStopWord
        fields = ["id", "word", "created_at", "created_by"]
        read_only_fields = ["id"]


class PostStopWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostStopWord
        fields = ["id", "word", "post", "created_at", "created_by"]
        read_only_fields = ["id"]
