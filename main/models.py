from django.db import models
from django.utils import timezone

# Create your models here.


class Magadel(models.Model):
    name = models.CharField('Название', max_length=300, null=False, blank=False)
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Магадель'
        verbose_name_plural = 'Магадель'
    def __str__(self):
        return f'{self.name} - {self.created_at} - {self.updated_at}'


class GroupProductDKCMagadel(models.Model):
    name = models.TextField('Описание', blank=False, null=False)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name




class ProductDKCMagadel(models.Model):
    code = models.CharField('Код', max_length=300, null=False, blank=False)
    name = models.TextField('Описание', blank=True, null=True)
    parent = models.ForeignKey(GroupProductDKCMagadel, related_name='products', on_delete=models.CASCADE)
    free_balance = models.FloatField('Свободный остаток', blank=True, null=True)
    list_possible_deliveries = models.TextField('Даты возможных поставок', blank=True, null=True)
    sum_possible_deliveries = models.FloatField('Сумма возможных поставок', blank=True, null=True)
    unit = models.CharField('ЕдИзм', max_length=300, null=True, blank=True, default='Не указано')
    def __str__(self):
        return f'{self.code} - {self.name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'