import json

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_celery_beat.models import PeriodicTask, CrontabSchedule


class BroadcastNotification(models.Model):
    message = models.TextField()
    broadcast_at = models.DateTimeField()
    sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-broadcast_at']


@receiver(post_save, sender=BroadcastNotification)
def notification_handler(sender, instance, created, **kwargs):
    # call group_send function directly to send notifications or you can create a dynamic task in celery beat

    if created:
        schedule, created = CrontabSchedule.objects.get_or_create(
            hour=instance.broadcast_at.hour,
            minute=instance.broadcast_at.minute,
            day_of_month=instance.broadcast_at.day,
            month_of_year=instance.broadcast_at.month,
        )

        task = PeriodicTask.objects.create(
            crontab=schedule,
            name='broadcast-notification-' + str(instance.id),
            task='notification_system.tasks.broadcast_notification',
            args=json.dumps((instance.id,))
        )
