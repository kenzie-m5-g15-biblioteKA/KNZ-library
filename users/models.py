from django.db import models
from django.contrib.auth.models import AbstractUser


class userOptions(models.TextChoices):
    Student = "Student"
    Staff = "Staff"


class userStatusOptions(models.TextChoices):
    Active = "Active"
    Blocked = "Blocked"


class User(AbstractUser):
    email = models.EmailField()
    Created_at = models.DateTimeField(auto_now_add=True)

    type_user = models.CharField(
        max_length=20,
        choices=userOptions.choices,
        default=userOptions.Student,
    )

    status = models.CharField(
        max_length=20,
        choices=userStatusOptions.choices,
        default=userStatusOptions.Active,
    )
