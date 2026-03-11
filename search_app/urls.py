from django.urls import path
from . import views

app_name = 'search_app'

urlpatterns = [
    path('', views.search, name='search'),
    path('suggestions/', views.search_suggestions, name='suggestions'),
]
