from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta

from lendings.models import Lending, LendingStatusChoice
from lendings.utils import working_day
from users.models import User, UserStatusChoice

scheduler = BackgroundScheduler()


def update_overdue_lendings() -> None:
    today = now().date()

    if working_day(today):
        lendings = Lending.objects.filter(status=LendingStatusChoice.LENT)

        for lending in lendings:
            db_user = User.objects.filter(pk=lending.user.pk)

            if lending and today > lending.return_date:
                lending_status = LendingStatusChoice.OVERDUE

                db_lending = Lending.objects.filter(pk=lending.pk)
                db_lending.update(status=lending_status, traffic_ticket="$50.00")

                if db_user:
                    user_data = db_user.first()

                    unblocked_date = today + timedelta(days=3)
                    while not working_day(unblocked_date):
                        unblocked_date += timedelta(days=1)
                    user_status = UserStatusChoice.BLOCKED

                    db_user.update(status=user_status, unblocked_date=unblocked_date)

                    send_mail(
                        subject="Bloqueio de empréstimos KNZ Library",
                        message="Sua conta agora está bloqueada impossibilitando o empréstimo de novos livros em nossa livraria por 3 dias úteis",
                        recipient_list=[user_data.email],
                        from_email=settings.EMAIL_HOST_USER,
                        fail_silently=False,
                    )


def schedule_overdue_check(hour: int = 0) -> None:
    scheduler.add_job(
        update_overdue_lendings, trigger="cron", hour=hour, id="overdue_check"
    )


def run_lending_scheduler() -> None:
    """run scheduler to auto update overdue lending status and apply user rules"""
    scheduler.start()
    schedule_overdue_check()


def reschedule_overdue_check(hour: int = 0) -> None:
    scheduler.reschedule_job("overdue_check", trigger="cron", hour=hour)


def stop_lending_scheduler() -> None:
    scheduler.shutdown()
