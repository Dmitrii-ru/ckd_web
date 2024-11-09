from django.contrib import admin
from django.urls import path, include
from .views import index, get_price , need_price

app_name = 'zaek'

urlpatterns = [
    path('', index, name='index'),
    path('get_price', get_price, name='get_price'),
    path('need_price', need_price , name='need_price')

]
