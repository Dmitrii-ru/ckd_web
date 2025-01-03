# Generated by Django 5.0.7 on 2024-11-29 21:25

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaek', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassificationPriceProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название ценовой категории')),
            ],
            options={
                'verbose_name': 'Ценовая категория',
                'verbose_name_plural': 'Ценовые категории',
            },
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название инструкции')),
                ('description', models.TextField(blank=True, verbose_name='Описание инструкции')),
            ],
            options={
                'verbose_name': 'Инструкция',
                'verbose_name_plural': 'Инструкции',
            },
        ),
        migrations.CreateModel(
            name='VolumeLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(unique=True, verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Градация объема',
                'verbose_name_plural': 'Градации объемов',
            },
        ),
        migrations.CreateModel(
            name='ZaekPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Прайс', max_length=100, unique=True, verbose_name='Название')),
                ('file', models.FileField(max_length=300, upload_to='files/', verbose_name='Файл')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Прайс',
                'verbose_name_plural': 'Прайс',
            },
        ),
        migrations.RemoveField(
            model_name='product',
            name='price_group',
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AddField(
            model_name='product',
            name='art',
            field=models.CharField(default='Нет данных', max_length=100, unique=True, verbose_name='Артикул'),
        ),
        migrations.AddField(
            model_name='product',
            name='level',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='nomenclature_group',
            field=models.CharField(blank=True, default='Нет данных', max_length=100, null=True, verbose_name='Номенклатурная группа'),
        ),
        migrations.AddField(
            model_name='product',
            name='packaging_norm',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Норма упаковки'),
        ),
        migrations.AddField(
            model_name='product',
            name='price_group_2',
            field=models.CharField(blank=True, default='Нет данных', max_length=100, null=True, verbose_name='Ценовая группа'),
        ),
        migrations.AddField(
            model_name='product',
            name='price_group_list',
            field=models.TextField(default='Нет данных', verbose_name='Список групп'),
        ),
        migrations.AddField(
            model_name='product',
            name='price_not_nds',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена (без НДС) руб.'),
        ),
        migrations.AddField(
            model_name='product',
            name='price_with_nds',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена (с НДС) руб.'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_portfolio',
            field=models.CharField(blank=True, default='Нет данных', max_length=100, null=True, verbose_name='Продуктовый портфель'),
        ),
        migrations.AddField(
            model_name='product',
            name='recommended_retail_price_not_nds',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Рекоменд. розничная цена (без НДС) руб.'),
        ),
        migrations.AddField(
            model_name='product',
            name='recommended_retail_price_with_nds',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Рекоменд. розничная цена (с НДС) руб.'),
        ),
        migrations.AddField(
            model_name='product',
            name='recommended_wholesale_price_not_nds',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Рекоменд. оптовая цена (без НДС) руб.'),
        ),
        migrations.AddField(
            model_name='product',
            name='recommended_wholesale_price_with_nds',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Рекоменд. оптовая цена (с НДС) руб.'),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_status_kursk',
            field=models.CharField(blank=True, default=0, max_length=100, null=True, verbose_name='Складской статус в Курске'),
        ),
        migrations.AddField(
            model_name='product',
            name='summary_price_group',
            field=models.CharField(blank=True, default='Нет данных', max_length=100, null=True, verbose_name='Ценовая группа сводная'),
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.CharField(default=0, max_length=20, verbose_name='Ед.'),
        ),
        migrations.AddField(
            model_name='product',
            name='volume',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Объем куб.м'),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Вес (кг)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.TextField(default='Нет данных', verbose_name='Номенклатура'),
        ),
        migrations.AddField(
            model_name='product',
            name='classification',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='zaek.classificationpriceproduct', verbose_name='Классификация ПП'),
        ),
        migrations.CreateModel(
            name='ClientClassificationDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.DecimalField(decimal_places=2, help_text='Скидка в процентах', max_digits=5, verbose_name='Скидка (%)')),
                ('classification_price_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classification_discounts', to='zaek.classificationpriceproduct', verbose_name='Название ценовой категории')),
            ],
            options={
                'verbose_name': 'Скидки типов клиентов',
                'verbose_name_plural': 'Скидка типа клиента',
            },
        ),
        migrations.CreateModel(
            name='InstructionStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.PositiveIntegerField(default=1, verbose_name='Номер шага')),
                ('photo', models.ImageField(blank=True, upload_to='instruction_photos/', verbose_name='Фото')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('instruction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='zaek.instruction', verbose_name='Инструкция')),
            ],
            options={
                'verbose_name': 'Шаг инструкции',
                'verbose_name_plural': 'Шаги инструкции',
                'unique_together': {('instruction', 'step')},
            },
        ),
        migrations.CreateModel(
            name='TypeClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=200, verbose_name='Тип клиента')),
                ('classification_price_products', models.ManyToManyField(related_name='type_clients', through='zaek.ClientClassificationDiscount', to='zaek.classificationpriceproduct', verbose_name='Классификации и скидки')),
            ],
            options={
                'verbose_name': 'Тип клиента',
                'verbose_name_plural': 'Типы клиентов',
            },
        ),
        migrations.AddField(
            model_name='clientclassificationdiscount',
            name='type_client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classification_discounts', to='zaek.typeclient', verbose_name='Тип клиента'),
        ),
        migrations.CreateModel(
            name='VolumeAtDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.DecimalField(decimal_places=2, help_text='Скидка в процентах', max_digits=5, verbose_name='Скидка (%)')),
                ('classification_price_product', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='classification_volume_discounts', to='zaek.classificationpriceproduct', verbose_name='Название ценовой категории')),
                ('type_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='volume_discounts', to='zaek.typeclient', verbose_name='Тип клиента')),
                ('volume_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='zaek.volumelevel', verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Скидка за объем',
                'verbose_name_plural': 'Скидки за объем',
            },
        ),
        migrations.DeleteModel(
            name='PriceGroup',
        ),
        migrations.AddConstraint(
            model_name='clientclassificationdiscount',
            constraint=models.UniqueConstraint(fields=('type_client', 'classification_price_product'), name='unique_type_client_classification'),
        ),
        migrations.AddConstraint(
            model_name='volumeatdiscount',
            constraint=models.UniqueConstraint(fields=('type_client', 'volume_level'), name='unique_type_client_volume_level'),
        ),
    ]
