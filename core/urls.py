from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from core.views import CommentView, PostImageView, PostView, UserView

router = DefaultRouter()
router.register("posts", PostView, basename="post")
router.register("comments", CommentView, basename="comment")
router.register("users", UserView, basename="user")

urlpatterns = [
    path(
        "api/docs/", SpectacularAPIView.as_view(), name="schema"
    ),  # загружает yaml файл
    path(
        "api/schema/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),  # ui страница для запросов
    path("admin/", admin.site.urls),
    path("posts/<int:pk>/image", PostImageView.as_view(), name="post-image"),
] + router.urls
