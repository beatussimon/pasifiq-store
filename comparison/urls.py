from django.urls import path
from . import views

app_name = 'comparison'

urlpatterns = [
    path('', views.comparison_view, name='view'),
    path('add/<int:product_id>/', views.add_to_comparison, name='add'),
    path('remove/<int:product_id>/', views.remove_from_comparison, name='remove'),
    path('clear/', views.clear_comparison, name='clear'),
]
