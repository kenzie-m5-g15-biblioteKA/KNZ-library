from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoleChoice(models.TextChoices):
    STUDENT = "student"
    STAFF = "staff"


class UserStatusChoice(models.TextChoices):
    ACTIVE = "Active"
    BLOCKED = "Blocked"


class User(AbstractUser):
    class Meta:
        ordering = ["id"]

    email = models.EmailField()

    role = models.CharField(
        max_length=20,
        choices=UserRoleChoice.choices,
        default=UserRoleChoice.STUDENT,
    )

    status = models.CharField(
        max_length=20,
        choices=UserStatusChoice.choices,
        default=UserStatusChoice.ACTIVE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    unblocked_date = models.DateField(null=True)
