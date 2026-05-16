from celery import shared_task
from users import services


@shared_task()
def checking_last_user_login():
    services.checking_last_login_date()


@shared_task
def blocking(users):
    services.blocking_user(users)
