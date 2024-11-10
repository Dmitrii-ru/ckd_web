from django.contrib import admin
from django.urls import path, include
from zaek.views import *

app_name = 'zaek'

urlpatterns = [
    path('', index, name='index'),
    path('get_price', get_price, name='get_price'),
    path('need_price', need_price , name='need_price'),
    path('price_menu_load', price_menu_load, name='price_menu_load'),
    path('get_price_groups', get_price_groups, name='get_price_groups'),
]


