from django.db import models


class Books(models.Model):
    class Meta:
        ordering = ["id"]

    name = models.CharField(max_length=255)
    published_date = models.DateField()

    followers = models.ManyToManyField(
        "users.User",
        related_name="Books",
        null=True,
    )
