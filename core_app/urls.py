from django.contrib import admin
from django.urls import path, include

from core_app import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main'))
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns