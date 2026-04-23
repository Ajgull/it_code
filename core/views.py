from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from core.filters import CommentFilter, PostFilter, UserFilter
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
from core.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
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
    queryset = Post.objects.filter(deleted__isnull=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def perform_create(
        self, serializer
    ):  # дополнительные действия при создании, класс CreateModelMixin
        serializer.save(author=self.request.user)

    def perform_destroy(
        instance,
    ):  # дополнительные действия при создании, класс DestroyModelMixin
        instance.status = "deleted"
        instance.deleted = timezone.now()
        instance.save()


class PostImageView(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = PostImageSerializer
    queryset = Post.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter


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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostStopWordView(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = PostStopWordSerializer
    queryset = PostStopWord.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class TagView(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
