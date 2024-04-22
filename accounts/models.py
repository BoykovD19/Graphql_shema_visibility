from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    username = models.CharField(max_length=60, default="", blank=True, unique=True)
    email = models.EmailField(
        null=False,
        blank=False,
        unique=True,
        db_index=True,
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()


class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_data = models.CharField(max_length=100)
