from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from core.views import (
    CategoryView,
    CommentView,
    GlobalStopWordView,
    PostImageView,
    PostStopWordView,
    PostView,
    TagView,
    UserView,
    VoteView,
)

router = DefaultRouter()
router.register("posts", PostView, basename="post")
router.register("comments", CommentView, basename="comment")
router.register("tags", TagView, basename="tags")
router.register("categories", CategoryView, basename="category")
router.register("users", UserView, basename="user")

urlpatterns = [
    path("admin/", admin.site.urls),
    # документация
    path("api/docs/", SpectacularAPIView.as_view(), name="schema"),  # save yaml file
    path(
        "api/schema/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),  # ui swagger
    # urls
    path("votes/", VoteView.as_view(), name="vote-list"),
    path(
        "global_stop_words/", GlobalStopWordView.as_view(), name="global_stop_word_list"
    ),
    path("post_stop_words/", PostStopWordView.as_view(), name="post_stop_word_list"),
    path("posts/<int:pk>/image/", PostImageView.as_view(), name="post_image"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls
