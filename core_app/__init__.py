from __future__ import absolute_import, unicode_literals

# Это заставляет Celery использовать настройки Django
from .celery import app as celery_app

# Убедитесь, что приложение Celery доступно при запуске Django
__all__ = ('celery_app',)