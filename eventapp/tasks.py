# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from .models import Event


@shared_task
def update_popular_events():
    updated_count = Event.objects.filter(
        public_count__gt=5,  # TODO update to 50
        is_popular=False
    ).update(is_popular=True)

    return f"{updated_count} events marked as popular"


@shared_task
def update_expired_events():
    today = timezone.localdate()

    updated_count = Event.objects.filter(
        date__lt=today,
        status="active"
    ).update(status="inactive")

    return f"{updated_count} expired events marked as inactive"