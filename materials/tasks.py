from celery import shared_task
from .services import newsletter_about_exposure, checking_changes


@shared_task
def sending_emails(course_id):
    newsletter_about_exposure(course_id)


@shared_task()
def checking_course_changes():
    checking_changes()
