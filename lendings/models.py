from datetime import date, timedelta

from django.db import models
from django.utils.timezone import now

from .utils import working_day


class Lending(models.Model):
    class Meta:
        ordering = ["id"]

    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="lendings",
    )
    copy = models.ForeignKey(
        "copies.Copy",
        on_delete=models.SET_NULL,
        related_name="lending",
    )

    lend_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True)

    def get_return_date(self) -> date:
        lend_date = now().date()
        lending_period = timedelta(days=15)
        return_date = lend_date + lending_period

        while not working_day(return_date):
            return_date += timedelta(days=1)

        return return_date
