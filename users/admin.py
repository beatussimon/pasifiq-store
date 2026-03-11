from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_store_owner', 'is_active')
    list_filter = ('is_store_owner', 'is_active', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Store Info', {'fields': ('bio', 'avatar', 'phone', 'location', 'is_store_owner')}),
    )
