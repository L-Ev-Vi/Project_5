from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    "checking_course_changes": {
        "task": "materials.tasks.checking_course_changes",
        "schedule": timedelta(hours=4),
    },
    "checking_last_user_login": {
        "task": "users.tasks.checking_last_user_login",
        "schedule": timedelta(days=30),
    },
}

app.autodiscover_tasks()
