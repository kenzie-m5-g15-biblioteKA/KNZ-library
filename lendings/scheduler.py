from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import now

from lendings.models import Lending, LendingStatusChoice

scheduler = BackgroundScheduler()


def update_overdue_lendings() -> None:
    lendings = Lending.objects.filter(status=LendingStatusChoice.LENT)
    today = now().date()

    for lending in lendings:
        if lending.return_date > today:
            lending.status = LendingStatusChoice.OVERDUE
            lending.save(update_fields=["status"])


def schedule_overdue_check() -> None:
    scheduler.add_job(
        update_overdue_lendings, trigger="cron", hour=0, id="overdue_check"
    )


def run_scheduler() -> None:
    """run scheduler to auto update overdue lending status"""
    scheduler.start()
    schedule_overdue_check()
