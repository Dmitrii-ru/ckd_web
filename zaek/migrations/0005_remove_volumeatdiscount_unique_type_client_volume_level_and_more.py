# Generated by Django 5.0.7 on 2025-01-11 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaek', '0004_alter_classificationpriceproduct_options_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='volumeatdiscount',
            name='unique_type_client_volume_level',
        ),
        migrations.AlterField(
            model_name='product',
            name='packaging_norm',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='Норма упаковки'),
        ),
        migrations.AlterField(
            model_name='volumelevel',
            name='stop_value',
            field=models.FloatField(blank=True, default=0, null=True, unique=True, verbose_name='До'),
        ),
        migrations.AddConstraint(
            model_name='volumeatdiscount',
            constraint=models.UniqueConstraint(fields=('classification_price_product', 'volume_level', 'type_client'), name='unique_type_client_volume_level'),
        ),
    ]
