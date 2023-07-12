from django.db import models


class Copy(models.Model):
    class Meta:
        ordering = ["id"]

    copies = models.IntegerField()
    description = models.CharField(max_length=255)

    book = models.ForeignKey(
        "books.Book",
        on_delete=models.CASCADE,
        related_name="copies",
    )
