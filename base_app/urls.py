from django.contrib import admin
from django.urls import path, include

from .views import start_page,get_currency

app_name = 'base_app'

urlpatterns = [
    path('', start_page, name='start_page'),
]
