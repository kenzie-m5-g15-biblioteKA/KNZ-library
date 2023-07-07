from django.db import models


class Assessments(models.Model):
    class Meta:
        ordering = ["id"]

    user = models.ForeignKey(
        "users.User",
        related_name="assessments",
        on_delete=models.CASCADE,
    )

    book = models.ForeignKey(
        "books.Book",
        related_name="assessments",
        on_delete=models.CASCADE,
    )

    comment = models.CharField(max_length=255, null=True)

    stars = models.IntegerField(default=0)
