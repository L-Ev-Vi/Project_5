from datetime import timedelta

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from config import settings
from users.models import Subscriptions
from .models import Course, Lesson
from django.utils import timezone


def newsletter_about_exposure(course_id):
    """Рассылка писем при обновлении материалов курса"""
    list_subscriptions = Subscriptions.objects.filter(course_id=course_id, subscription=True)
    recipient_list = [subscription.user.email for subscription in list_subscriptions]
    course = get_object_or_404(Course, pk=course_id)
    subject = "Уведомление!"
    message = f"Материалы курса '{course.title}' обновились, перейдите в личный кабинет для просмотра изменений."
    try:
        # отправка письма на адреса электронной почты подписанных пользователей
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    except Exception as e:
        print(f"error: {str(e)}")


def sending_notification(message, email):
    """Рассылка уведомлений"""
    recipient_list = [email]
    subject = "Уведомление!"
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    except Exception as e:
        print(f"error: {str(e)}")


def checking_changes():
    """Проверка обновления материалов курса"""
    list_course = Course.objects.all()
    four_clock = timedelta(hours=4)
    current_datetime = timezone.localtime(timezone.now())
    for course in list_course:
        message = None
        lessons = course.lesson
        for lessen in lessons.all():
            if (current_datetime - lessen.update_at) > four_clock:
                message = f"Курс '{course.title}' не обновлялся более 4-х часов!"
                email = course.author.email
                sending_notification(message, email)
                break
        if message is None:
            if (current_datetime - course.update_at) > four_clock:
                message = f"Курс '{course.title}' не обновлялся более 4-х часов!"
                email = course.author.email
                sending_notification(message, email)
