from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views import CommentView, PostView, UserView

router = DefaultRouter()
router.register("posts", PostView, basename="post")
router.register("comments", CommentView, basename="comment")
router.register("users", UserView, basename="user")

urlpatterns = [
    path("admin/", admin.site.urls),
] + router.urls
