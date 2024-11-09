from django.db import models
from django.utils import timezone

# class PriceGroup(models.Model):
#     # Поле для хранения ссылки на родителя
#     parent = models.ForeignKey(
#         'self',  # Ссылка на саму модель
#         on_delete=models.CASCADE,  # Удаление родителя приводит к удалению всех его детей
#         null=True,  # У родителя может не быть родителя
#         blank=True,  # Поле может быть пустым
#         related_name='group'  # Имя для обратной связи (children) у родителя
#     )
#
#     name = models.CharField(max_length=100)  # Пример поля для имени родителя
#     level = models.IntegerField(blank=False,null=False,default=0)
#     # Другие поля для информации о родителе могут быть добавлены здесь
#
#     def __str__(self):
#         parent_str = f", parent== {self.parent.name}" if self.parent else ""
#         return f'{"-" * self.level,self.level} {self.name} {parent_str}'


class Product(models.Model):

    price_group_list = models.TextField(
        verbose_name='Список групп',
        default='Нет данных'
    )

    level = models.IntegerField(blank=False, null=False, default=0)
    name = models.TextField(
        verbose_name='Номенклатура',
        default='Нет данных'
    )
    art = models.CharField(
        max_length=100,
        verbose_name='Артикул',
        unique=True,
        default='Нет данных'
    )
    unit = models.CharField(
        verbose_name='Ед.',
        max_length=20,
        default=0
    )

    price_not_nds = models.DecimalField(
        verbose_name='Цена (без НДС) руб.',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    price_with_nds = models.DecimalField(
        verbose_name='Цена (с НДС) руб.',
        max_digits=10,
        decimal_places=2,
        default=0
    )

    recommended_wholesale_price_not_nds = models.DecimalField(
        verbose_name='Рекоменд. оптовая цена (без НДС) руб.',
        max_digits=10,
        decimal_places=2,
        default=0

    )
    recommended_wholesale_price_with_nds = models.DecimalField(
        verbose_name='Рекоменд. оптовая цена (с НДС) руб.',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    recommended_retail_price_not_nds = models.DecimalField(
        verbose_name='Рекоменд. розничная цена (без НДС) руб.',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    recommended_retail_price_with_nds = models.DecimalField(
        verbose_name='Рекоменд. розничная цена (с НДС) руб.',
        max_digits=10,
        decimal_places=2,
        default=0
    )

    stock_status_kursk = models.CharField(
        verbose_name='Складской статус в Курске',
        max_length=100,
        blank=True,
        null=True,
        default=0
    )
    volume = models.FloatField(
        verbose_name='Объем куб.м',

        blank=True,
        null=True,
        default=0
    )
    weight = models.FloatField(
        verbose_name='Вес (кг)',

        blank=True,
        null=True,
        default=0
    )

    product_portfolio = models.CharField(
        verbose_name='Продуктовый портфель',
        max_length=100,
        blank=True,
        null=True,
        default='Нет данных'
    )
    packaging_norm = models.IntegerField(
        verbose_name='Норма упаковки',
        blank=True,
        null=True,
        default=0

    )
    nomenclature_group = models.CharField(
        verbose_name='Номенклатурная группа',
        max_length=100,
        blank=True,
        null=True,
        default='Нет данных'
    )

    price_group_2 = models.CharField(
        verbose_name='Ценовая группа',
        max_length = 100,
        blank=True,
        null=True,
        default='Нет данных'
    )

    summary_price_group = models.CharField(
        verbose_name='Ценовая группа сводная',
        max_length = 100,
        blank=True,
        null=True,
        default='Нет данных'
    )

    classification = models.CharField(
        verbose_name='Классификация ПП',
        max_length = 100,
        blank=True,
        null=True,
        default='Нет данных'
    )


    def __str__(self):
        return f'{self.art} '



class ZaekPrice(models.Model):
    file = models.FileField('Файл',upload_to='files/' , max_length=300, null=False, blank=False)
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Прайс'
        verbose_name_plural = 'Прайс'


    def __str__(self):
        return f'{self.name} - {self.created_at} - {self.updated_at}'