from django.db import models

from books.models import Book


class Copy(models.Model):
    class Meta:
        ordering = ["id"]

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )
    copies = models.PositiveIntegerField()
    description = models.CharField(max_length=255)

    # def __str__(self):
    #     return f"{self.quantity} copies of {self.book.name}"
