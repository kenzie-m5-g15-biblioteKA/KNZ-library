from django.db import models
from books.models import Books


class Copies(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} copies of {self.book.name}"
