from django.db import models


class AvailabilityOptions(models.TextChoices):
    unavailable = "unavaliable"
    avaliable = "avaliable"


class Book(models.Model):
    class Meta:
        ordering = ["id"]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    publishing_company = models.CharField(max_length=100)

    availability = models.CharField(
        max_length=255,
        choices=AvailabilityOptions.choices,
        default=AvailabilityOptions.avaliable,
    )

    ranking = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
    )

    followers = models.ManyToManyField(
        "users.User",
        related_name="Books",
    )
