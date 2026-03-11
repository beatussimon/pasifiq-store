from django.db import models
from django.conf import settings

class ProductView(models.Model):
    product = models.ForeignKey('products.Product', related_name='view_records', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    referrer = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_views'
        indexes = [models.Index(fields=['product', '-created_at'])]

class DailyStats(models.Model):
    date = models.DateField(unique=True)
    total_views = models.PositiveIntegerField(default=0)
    total_inquiries = models.PositiveIntegerField(default=0)
    new_users = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'daily_stats'
        ordering = ['-date']
