from datetime import date, timedelta

from django.db import models
from django.utils.timezone import now

from .utils import working_day


class LendingStatusChoice(models.TextChoices):
    LENT = "lent"
    OVERDUE = "overdue"
    RETURNED = "returned"


class Lending(models.Model):
    class Meta:
        ordering = ["id"]

    user = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, related_name="lendings", null=True
    )
    copy = models.ForeignKey("copies.Copy", on_delete=models.SET_NULL, null=True)

    lend_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True)
    returned_date = models.DateField(null=True)

    status = models.CharField(
        max_length=10,
        choices=LendingStatusChoice.choices,
        default=LendingStatusChoice.LENT,
    )

    def get_return_date(self) -> date:
        lend_date = now().date()
        lending_period = timedelta(days=15)
        return_date = lend_date + lending_period

        while not working_day(return_date):
            return_date += timedelta(days=1)

        return return_date

    def get_return_book(self) -> None:
        today = now().date()

        self.returned_date = today
        self.status = LendingStatusChoice.RETURNED
        self.save()

    def get_status(self) -> None:
        today = now().date()

        if today > self.return_date and self.status != LendingStatusChoice.RETURNED:
            self.status = LendingStatusChoice.OVERDUE
            self.save()
