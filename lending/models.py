from django.db import models


class Lending(models.Model):
    class Meta:
        ordering = ["id"]

    created_at = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField()
    returned_date = models.DateField(null=True)

    user = models.ForeignKey(
        "users.User",
        related_name="lending",
        on_delete=models.CASCADE,
    )

    copy = models.ForeignKey(
        "copies.Copy",
        related_name="lending",
        on_delete=models.CASCADE,
    )
