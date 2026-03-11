from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'product', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('sender_name', 'sender_email', 'content')
    readonly_fields = ('created_at', 'ip_address')
