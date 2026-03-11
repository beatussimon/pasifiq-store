from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('products/<int:pk>/toggle-featured/', views.toggle_featured, name='toggle_featured'),
    path('products/<int:product_id>/images/', views.product_images, name='product_images'),
    path('products/images/<int:image_id>/delete/', views.delete_image, name='delete_image'),
    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('messages/<int:pk>/archive/', views.archive_message, name='archive_message'),
    path('users/', views.user_list, name='user_list'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('settings/', views.store_settings, name='settings'),
]
