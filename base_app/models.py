from django.db import models
from django.utils import timezone


class ErrorData(models.Model):
    name = models.CharField('Название функции', max_length=230, null=False, blank=False, default='///')
    path = models.TextField('Путь', default='///')
    error  = models.TextField('Ошибка', default='///')
    created_at = models.DateTimeField('Дата создания', default=timezone.now)

    def __str__(self):
        return f'{self.error}  / / / {self.name} / / / {self.path} / / / {self.created_at}'
