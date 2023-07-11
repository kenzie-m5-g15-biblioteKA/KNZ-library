from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta

from lendings.utils import working_day
from users.models import User, UserStatusChoice

scheduler = BackgroundScheduler()


def unblock_users() -> None:
    today = now().date()

    if working_day(today):
        blocked_users = User.objects.filter(status=UserStatusChoice.BLOCKED)

        for user in blocked_users:
            if user and today >= user.unblocked_date:
                user_data = db_user.first()

                user_status = UserStatusChoice.ACTIVE

                db_user = User.objects.filter(pk=user.pk)
                db_user.update(status=user_status, unblocked_date=None)

                send_mail(
                    subject="Desbloqueio de empréstimos KNZ Library",
                    message="Sua conta foi desbloqueada, já pode voltar a realizar empréstimos em nossa livraria aproveite!!",
                    recipient_list=[user_data.email],
                    from_email=settings.EMAIL_HOST_USER,
                    fail_silently=False,
                )


def schedule_unblock_users(hour: int = 0) -> None:
    scheduler.add_job(unblock_users, trigger="cron", hour=hour, id="unblock_users")


def run_user_scheduler() -> None:
    """run scheduler to auto unblock user after unblock_date"""
    scheduler.start()
    schedule_unblock_users()


def reschedule_unblock_user(hour: int = 0) -> None:
    scheduler.reschedule_job("unblock_users", trigger="cron", hour=hour)


def stop_user_scheduler() -> None:
    scheduler.shutdown()
