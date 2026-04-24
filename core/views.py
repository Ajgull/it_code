from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

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
    CustomTokenSerializer,
    GlobalStopWordSerializer,
    PostImageSerializer,
    PostSerializer,
    PostStopWordSerializer,
    TagSerializer,
    UserCreateSerializer,
    UserSerializer,
    VoteSerializer,
)


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        return Response(serializer.validated_data)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    def post(self, request: Request, *args: object, **kwargs: object) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message': 'user created',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(deleted__isnull=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def perform_create(self, serializer) -> None:  # дополнительные действия при создании, класс CreateModelMixin
        serializer.save(author=self.request.user)

    def perform_destroy(
        self,
        instance: object,
    ) -> None:  # дополнительные действия при создании, класс DestroyModelMixin
        instance.status = 'deleted'
        instance.deleted = timezone.now()
        instance.save()


class PostImageView(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = PostImageSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def post(self, request: Request, *args: object, **kwargs: object) -> None:
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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request: Request, *args: object, **kwargs: object) -> None:
        return self.create(request, *args, **kwargs)


class GlobalStopWordView(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = GlobalStopWordSerializer
    queryset = GlobalStopWord.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer) -> None:
        serializer.save(created_by=self.request.user)

    def post(self, request: Request, *args: object, **kwargs: object) -> None:
        return self.create(request, *args, **kwargs)


class PostStopWordView(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = PostStopWordSerializer
    queryset = PostStopWord.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def post(self, request: Request, *args: object, **kwargs: object) -> None:
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
