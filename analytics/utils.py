from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate
from .models import ProductView, DailyStats
from messaging.models import Message
from users.models import CustomUser

def get_daily_stats(days_count=7):
    now = timezone.now()
    start_date = (now - timedelta(days=days_count - 1)).date()
    
    # Get pre-aggregated stats
    stats_qs = DailyStats.objects.filter(date__gte=start_date).values('date', 'total_views', 'total_inquiries', 'new_users')
    stats_dict = {s['date']: s for s in stats_qs}

    days = []
    views_data = []
    inquiries_data = []
    registrations_data = []
    
    for i in range(days_count - 1, -1, -1):
        day = (now - timedelta(days=i)).date()
        days.append(day.strftime('%b %d'))
        day_stats = stats_dict.get(day, {'total_views': 0, 'total_inquiries': 0, 'new_users': 0})
        views_data.append(day_stats['total_views'])
        inquiries_data.append(day_stats['total_inquiries'])
        registrations_data.append(day_stats['new_users'])
        
    return {
        'days': days,
        'views': views_data,
        'inquiries': inquiries_data,
        'registrations': registrations_data,
    }
