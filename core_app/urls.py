from django.contrib import admin
from django.urls import path, include

from core_app import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base_app.urls', namespace='base_app')),
    path('ckd', include('ckd.urls', namespace='ckd')),
    path('zaek/', include('zaek.urls', namespace='zaek')),
    path('stock', include('stock.urls', namespace='stock')),
]



if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns