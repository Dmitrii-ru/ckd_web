from django.db import models
from django.utils import timezone


class ClassificationPriceProduct(models.Model):
    """Ценовая категория"""
    name = models.CharField("Название ценовой категории", max_length=200)

    class Meta:
        verbose_name = 'Ценовая категория'
        verbose_name_plural = '2.1 Ценовые категории'


    def __str__(self):
        return self.name


class TypeClient(models.Model):
    """Тип клиента"""
    type = models.CharField("Тип клиента", max_length=200)
    classification_price_products = models.ManyToManyField(
        ClassificationPriceProduct,
        through='ClientClassificationDiscount',
        related_name='type_clients',
        verbose_name='Классификации и скидки'
    )

    class Meta:
        verbose_name = 'Тип клиента'
        verbose_name_plural = '1.1 Типы клиентов'


    def __str__(self):
        return self.type




class ClientClassificationDiscount(models.Model):
    """Стандартные скидки типа клиента"""


    type_client = models.ForeignKey(
        TypeClient,
        verbose_name="Тип клиента",
        on_delete=models.CASCADE,
        related_name='classification_discounts'
    )
    classification_price_product = models.ForeignKey(
        ClassificationPriceProduct,
        verbose_name="Название ценовой категории",
        on_delete=models.CASCADE,
        related_name='classification_discounts'
    )
    discount = models.DecimalField(
        "Скидка (%)",
        max_digits=5,
        decimal_places=2,
        help_text="Скидка в процентах"
    )


    class Meta:

        ''' Уникальные сочинение типа клина и Название ценовой категории'''

        verbose_name = 'Скидки типов клиентов'
        verbose_name_plural = '3.1 Скидка типа клиента'

        constraints = [
            models.UniqueConstraint(
                fields=['type_client', 'classification_price_product'],
                name='unique_type_client_classification'
            )
        ]


    def __str__(self):
        return f'{self.type_client} - {self.classification_price_product} - {self.discount}'





"""______________________________________________________________________________________________________"""

class VolumeLevel(models.Model):
    """Виды скидок от объема"""

    start_value = models.FloatField(
        verbose_name='От',
        unique=True,
        blank=False,
        default=0
    )

    stop_value = models.FloatField(
        verbose_name='До',
        unique=True,
        blank=False,
        default=0
    )


    class Meta:
        verbose_name = 'Градация объема'
        verbose_name_plural = '4.1 Градации объемов'

    def __str__(self):
        return f'От {  str(self.start_value)} - До {str(self.stop_value)}'


class VolumeAtDiscount(models.Model):
    """Скидки от объема, вида клиента, и ценовой категории. """


    type_client = models.ForeignKey(
        TypeClient,
        verbose_name="Тип клиента",
        on_delete=models.CASCADE,
        related_name='volume_discounts'
    )

    volume_level = models.ForeignKey(
        VolumeLevel,
        verbose_name="Значение",
        on_delete=models.CASCADE,
        related_name='discounts'
    )

    classification_price_product = models.ForeignKey(
        ClassificationPriceProduct,
        verbose_name="Название ценовой категории",
        on_delete=models.CASCADE,
        related_name='classification_volume_discounts',
        null=True,
        blank=True,
        default=1

    )
    
    discount = models.DecimalField(
        "Скидка (%)",
        max_digits=5,
        decimal_places=2,
        help_text="Скидка в процентах"
    )


    class Meta:

        ''' Уникальные сочинение типа клина и объем'''

        verbose_name = 'Скидка за объем'
        verbose_name_plural = '3.2 Скидки за объем'

        constraints = [
            models.UniqueConstraint(
                fields=['type_client', 'volume_level'],
                name='unique_type_client_volume_level'
            )
        ]
    

    def __str__(self):
        return (
            f'{self.type_client} '
            f'{self.volume_level} '
            f'{self.classification_price_product} '
            f'{self.discount} '
        )



class Product(models.Model):

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    classification = models.ForeignKey(
        ClassificationPriceProduct,
        verbose_name= 'Классификация ПП',
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT
    )


    price_group_list = models.TextField(
        verbose_name='Список групп',
        default='Нет данных'
    )

    level = models.IntegerField(
        blank=False,
        null=False,
        default=0
    )
    
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



    def __str__(self):
        return f'{self.art} '



class ZaekPrice(models.Model):
    name = models.CharField('Название', max_length=100, unique=True, null=False, blank=False, default='Прайс')
    file = models.FileField('Файл', upload_to='files/', max_length=300, null=False, blank=False)
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Прайс'
        verbose_name_plural = 'Прайс'


    def __str__(self):
        return f'{self.name} - {self.created_at} - {self.updated_at}'




class Instruction(models.Model):
    title = models.CharField("Название инструкции", max_length=200)
    description = models.TextField("Описание инструкции", blank=True)

    class Meta:
        verbose_name = 'Инструкция'
        verbose_name_plural = 'Инструкции'

    def __str__(self):
        return self.title


class InstructionStep(models.Model):
    instruction = models.ForeignKey(
        Instruction,
        on_delete=models.CASCADE,
        related_name="steps",
        verbose_name="Инструкция"
    )
    step = models.PositiveIntegerField(verbose_name='Номер шага', blank=False, default=1)
    photo = models.ImageField("Фото", upload_to="instruction_photos/",blank=True)
    comment = models.TextField("Комментарий", blank=True)

    class Meta:
        unique_together = ('instruction', 'step')
        verbose_name = "Шаг инструкции"
        verbose_name_plural = "Шаги инструкции"

    def __str__(self):
        return f"Шаг {self.step} для {self.instruction.title}"

