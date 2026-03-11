from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import CustomUser
from messaging.models import Message
from .models import DailyStats
from django.db import models

@receiver(post_save, sender=CustomUser)
def track_new_user(sender, instance, created, **kwargs):
    if created:
        today = timezone.now().date()
        stats, _ = DailyStats.objects.get_or_create(date=today)
        DailyStats.objects.filter(pk=stats.pk).update(new_users=models.F('new_users') + 1)

@receiver(post_save, sender=Message)
def track_new_inquiry(sender, instance, created, **kwargs):
    if created:
        today = timezone.now().date()
        stats, _ = DailyStats.objects.get_or_create(date=today)
        DailyStats.objects.filter(pk=stats.pk).update(total_inquiries=models.F('total_inquiries') + 1)
