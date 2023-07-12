from django.apps import AppConfig


class LendingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lendings"

    def ready(self) -> None:
        from lendings.scheduler import run_lending_scheduler
        from users.scheduler import run_user_scheduler

        run_lending_scheduler()
        un_user_scheduler()
