from django.db import models


class AvailabilityChoice(models.TextChoices):
    unavailable = "unavailable"
    available = "available"


class Book(models.Model):
    class Meta:
        ordering = ["id"]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    publishing_company = models.CharField(max_length=100)
    availability = models.CharField(
        max_length=255,
        choices=AvailabilityChoice.choices,
        default=AvailabilityChoice.available,
    )

    followers = models.ManyToManyField(
        "users.User",
        related_name="Books",
    )
