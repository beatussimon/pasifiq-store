from django.contrib import admin
from .models import ProductView, DailyStats

@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_views', 'total_inquiries', 'new_users')
    readonly_fields = ('date', 'total_views', 'total_inquiries', 'new_users')
