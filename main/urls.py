from django.contrib import admin
from django.urls import path, include

from .views import index, upload_maga,find_products_code

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('upload_maga', upload_maga, name="upload_maga"),
    path('find_products_code',find_products_code,name='find_products_code')
]
