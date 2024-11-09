from django.contrib import admin
from django.urls import path, include

from .views import stock_data

app_name = 'stock'

urlpatterns = [
    path('', stock_data, name='index'),
]
