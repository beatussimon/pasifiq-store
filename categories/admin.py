from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'product_count', 'is_active', 'sort_order')
    list_filter = ('is_active', 'parent')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
