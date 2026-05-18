from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from config import settings
from users.models import Subscriptions

from .models import Course, Lesson


@shared_task
def newsletter_about_updates(id, obj):
    """Рассылка писем при обновлении материалов курса"""
    if obj == "course":
        list_subscriptions = Subscriptions.objects.filter(course_id=id, subscription=True)
        course = get_object_or_404(Course, pk=id)
        recipient_list = [subscription.user.email for subscription in list_subscriptions]
        subject = "Уведомление!"
        message = f"Материалы курса '{course.title}' обновились, перейдите в личный кабинет для просмотра изменений."
        run_at = course.update_at + timedelta(hours=4)
        sending_emails.apply_async(args=[subject, message, recipient_list], eta=run_at)
    else:
        lesson = Lesson.objects.get(pk=id)
        course_list = lesson.courses.all()
        for course in course_list:
            list_subscriptions = Subscriptions.objects.filter(course_id=course.pk, subscription=True)
            recipient_list = [subscription.user.email for subscription in list_subscriptions]
            subject = "Уведомление!"
            message = (
                f"Материалы курса '{course.title}' обновились, перейдите в личный кабинет для просмотра изменений."
            )
            run_at = lesson.update_at + timedelta(hours=4)
            print(run_at)
            sending_emails.apply_async(args=[subject, message, recipient_list], eta=run_at)


@shared_task()
def sending_emails(subject, message, recipient_list):
    """Рассылка уведомлений"""
    try:
        # отправка письма на адреса электронной почты подписанных пользователей
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    except Exception as e:
        print(f"error: {str(e)}")
