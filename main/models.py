from django.db import models


# Create your models here.


class Magadel(models.Model):
    name = models.CharField('Название', max_length=300, null=False, blank=False)


class GroupProductDKCMagadel(models.Model):
    name = models.TextField('Описание', blank=False, null=False)

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
