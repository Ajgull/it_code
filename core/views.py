from rest_framework import generics, mixins, viewsets

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
from core.serializers import (
    CategorySerializer,
    CommentSerializer,
    GlobalStopWordSerializer,
    PostImageSerializer,
    PostSerializer,
    PostStopWordSerializer,
    TagSerializer,
    UserSerializer,
    VoteSerializer,
)


class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostImageView(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = PostImageSerializer
    queryset = Post.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class VoteView(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class GlobalStopWordView(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = GlobalStopWordSerializer
    queryset = GlobalStopWord.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostStopWordView(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = PostStopWordSerializer
    queryset = PostStopWord.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class TagView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
