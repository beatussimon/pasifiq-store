from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'condition', 'status', 'price', 'is_featured', 'view_count', 'created_at')
    list_filter = ('status', 'condition', 'is_featured', 'category')
    search_fields = ('name', 'description', 'tags')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    list_editable = ('is_featured', 'status')
    readonly_fields = ('view_count', 'wishlist_count', 'comparison_count', 'inquiry_count', 'average_rating')
