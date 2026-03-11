from django.urls import path
from . import views

app_name = 'ratings'

urlpatterns = [
    path('rate/<int:product_id>/', views.rate_product, name='rate'),
]
