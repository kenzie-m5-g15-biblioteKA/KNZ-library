from django.contrib.auth.models import AbstractUser
from django.db import models


class userOptions(models.TextChoices):
    STUDENT = "Student"
    STAFF = "Staff"


class userStatusOptions(models.TextChoices):
    ACTIVE = "Active"
    BLOCKED = "Blocked"


class User(AbstractUser):
    class Meta:
        ordering = ["id"]

    email = models.EmailField()

    role = models.CharField(
        max_length=20,
        choices=userOptions.choices,
        default=userOptions.STUDENT,
    )

    status = models.CharField(
        max_length=20,
        choices=userStatusOptions.choices,
        default=userStatusOptions.ACTIVE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    unblocked_date = models.DateField(null=True)
