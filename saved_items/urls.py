from django.urls import path
from . import views

app_name = 'saved_items'

urlpatterns = [
    path('', views.saved_list, name='list'),
    path('toggle/<int:product_id>/', views.toggle_saved, name='toggle'),
]
