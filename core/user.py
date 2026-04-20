from django.contrib.auth.models import AbstractUser
from django.db import models

from core.consts import ROLE_CHOICES


class User(AbstractUser):
    username = models.CharField(
        verbose_name="name", blank=False, max_length=50, unique=True
    )
    email = models.EmailField(verbose_name="email", blank=False, max_length=255)
    password = models.CharField("passsword", blank=False, max_length=100)
    role = models.CharField(choices=ROLE_CHOICES, verbose_name="role")
    avatar = models.ImageField(
        upload_to="avatars/",
        verbose_name="avatar",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(verbose_name="active", default=False)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["username"]

    def __str__(self) -> str:
        return f"User {self.username}, email - {self.email}"
