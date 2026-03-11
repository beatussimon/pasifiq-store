from django.db import models
from django.utils import timezone
from .models import DailyStats

class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.session_key:
            request.session.create()
        
        # Track visit in DailyStats (simple version)
        if not request.path.startswith('/static/') and not request.path.startswith('/media/'):
            today = timezone.now().date()
            stats, created = DailyStats.objects.get_or_create(date=today)
            DailyStats.objects.filter(pk=stats.pk).update(total_views=models.F('total_views') + 1)
        
        response = self.get_response(request)
        return response
