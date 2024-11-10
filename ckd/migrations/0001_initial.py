# Generated by Django 5.0.7 on 2024-08-03 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GroupProductDKCMagadel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='Magadel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='ProductDKCMagadel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=300, verbose_name='Код')),
                ('name', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='ckd.groupproductdkcmagadel')),
            ],
        ),
    ]
