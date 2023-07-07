from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoleChoice(models.TextChoices):
    student = "student"
    staff = "staff"


class UserStatusChoice(models.TextChoices):
    active = "active"
    blocked = "blocked"


class User(AbstractUser):
    class Meta:
        ordering = ["id"]

    created_at = models.DateTimeField(auto_now_add=True)

    role = models.CharField(
        max_length=10,
        choices=UserRoleChoice.choices,
        default=UserRoleChoice.student,
    )

    status = models.CharField(
        max_length=10,
        choices=UserStatusChoice.choices,
        default=UserStatusChoice.active,
    )
