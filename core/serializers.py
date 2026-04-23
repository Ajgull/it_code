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
from core.service import calculate_comment_depth


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
    post_id = serializers.IntegerField(write_only=True, required=True)
    parent_comment_id = serializers.IntegerField(
        write_only=True, required=False, allow_null=True, default=None
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "author",
            "post_id",
            "parent_comment_id",
            "parent_comment",
            "tags",
            "depth_level",
        ]
        read_only_fields = ["id", "author", "depth_level", "parent_comment"]

    def create(self, validated_data):

        user = self.context["request"].user
        post_id = validated_data.pop("post_id")
        parent_comment_id = validated_data.pop("parent_comment_id", None)
        tags = validated_data.pop("tags", [])

        post = Post.objects.get(id=post_id)
        parent_comment = None
        if parent_comment_id:
            parent_comment = Comment.objects.get(id=parent_comment_id)

        depth_level = calculate_comment_depth(parent_comment)

        comment = Comment.objects.create(
            author=user,
            post=post,
            parent_comment=parent_comment,
            depth_level=depth_level,
            **validated_data,
        )

        if tags:
            comment.tags.set(tags)
        return comment


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "user", "post", "comment", "vote_type"]
        read_only_fields = ["id"]


class GlobalStopWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalStopWord
        fields = ["id", "word", "created_at", "created_by"]
        read_only_fields = ["id", "created_by"]


class PostStopWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostStopWord
        fields = ["id", "word", "post", "created_at", "created_by"]
        read_only_fields = ["id"]
