from django.contrib import admin
from django.urls import path, include
from zaek.views import *
from django.conf import settings
from django.conf.urls.static import static
app_name = 'zaek'

urlpatterns = [
    path('', index, name='index'),
    path('get_price', get_price, name='get_price'),

    path('pml', price_menu_load, name='pml'),
    path('dmp', data_menu_processing, name='dmp'),
    path('dmp/find_objects_in_load_excel',func_find_objects_view,name= 'find_objects_in_load_excel'),
    path('dmp/need_price', need_price , name='need_price'),
    path('get_price_groups', get_price_groups, name='get_price_groups'),
    path('consolidated_table',consolidated_table,name='consolidated_table'),
    path('instructions/', InstructionListView.as_view(), name='instruction_list'),
    path('instruction/<int:pk>/', InstructionDetailView.as_view(), name='instruction_detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


