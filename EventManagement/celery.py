# project/celery.py

import os

from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "EventManagement.settings"
)

app = Celery("project")

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)

app.autodiscover_tasks()

from celery.schedules import crontab

app.conf.beat_schedule = {
    "expire-pending-bookings": {
        "task": "logicapp.tasks.expire_bookings",
         "schedule": crontab(minute="*/1")
    },
    "update-popular-events-every-5-minutes": {
        "task": "eventapp.tasks.update_popular_events",
        "schedule": crontab(minute="*/5"),
    },
    "update-expired-events-every-5-minutes": {
        "task": "eventapp.tasks.update_expired_events",
        "schedule": 300.0,  # Every 5 minutes
    },
}