from django.db import models
from django.contrib.auth.models import AbstractUser


class userOptions(models.TextChoices):
    Student = "Student"
    Collaborator = "Collaborator"


class User(AbstractUser):
    type_user = models.CharField(
        max_length=20,
        choices=userOptions.choices,
        default=userOptions.Student,
    )
    # Created_at = models.DateTimeField(auto_now_add=True)
