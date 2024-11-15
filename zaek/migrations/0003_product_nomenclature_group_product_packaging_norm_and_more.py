# Generated by Django 5.0.7 on 2024-10-28 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaek', '0002_product_art_alter_product_name'),
    ]

    operations = [
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
            name='unit',
            field=models.CharField(default=0, max_length=20, verbose_name='Ед.'),
        ),
        migrations.AddField(
            model_name='product',
            name='volume',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=8, null=True, verbose_name='Объем куб.м'),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True, verbose_name='Вес (кг)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='art',
            field=models.TextField(default='Нет данных', unique=True, verbose_name='Артикул'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.TextField(default='Нет данных', verbose_name='Номенклатура'),
        ),
    ]
