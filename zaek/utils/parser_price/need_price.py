import os
import openpyxl
from zaek.models import Product
from zaek.consts_zaek import attrs_update_products, split_parent_base, split_parent_obj, custom_price_name
import pandas as pd
import io
from django.core.files.base import ContentFile
from zaek.models import ZaekPrice
from django.utils import timezone
from base_app.utils.errors_plase import create_error


class CreatePriceExcel:

    def __init__(
            self,
            model = Product,
            attrs_update = attrs_update_products,
            custom_price_name = custom_price_name

    ):
        self.custom_price_name = custom_price_name
        self.model = model
        self.attrs_update = attrs_update
        self.level_columns = {}
        self.object= None
        self.new_object = {}
        self.list_ready_ty_excel =[]
        self.columns_1 = [
            'Артикул', 'Номенклатура', 'Ед.',
            'Цена (без НДС) руб.', 'Цена (с НДС) руб.',
            'Классификация ПП'


        ]
        self.columns_2 = [
            'Рекоменд. оптовая цена (без НДС) руб.', 'Рекоменд. оптовая цена (с НДС) руб.',
            'Рекоменд. розничная цена (без НДС) руб.', 'Рекоменд. розничная цена (с НДС) руб.',
            'Складской статус в Курске', 'Объем куб.м', 'Вес (кг)',
            'Продуктовый портфель', 'Норма упаковки', 'Номенклатурная группа',
            'Ценовая группа','Ценовая группа сводная'
        ]
        self.price = None


    def get_level_value(self,value):
        for l_value in value.split(split_parent_base):
            level_value = l_value.split(split_parent_obj)
            level = int(level_value[0])
            value = level_value[1]
            self.level_columns[level]= f'Уровень: {level}'
            self.new_object[f'Уровень: {level}'] = value


    def parsing_object(self):
        for attr in self.attrs_update:
            if attr == 'price_group_list':
                value = getattr(self.object, attr, None)
                if value:
                    self.get_level_value(value)
            else:
                value = getattr(self.object, attr, None)
                key = self.object._meta.get_field(f'{attr}').verbose_name


                self.new_object[key] = value


    def get_product_all(self):

        self.list_ready_ty_excel = []
        objects_all = self.model.objects.all()
        for obj in objects_all:
            self.object = obj
            self.parsing_object()
            self.list_ready_ty_excel.append(self.new_object)
            self.new_object = {}
        self.write_to_excel()
        return self.price

    def write_to_excel(self):
        sorted_columns = [self.level_columns[key] for key in sorted(self.level_columns.keys())]
        all_columns = self.columns_1 + sorted_columns + self.columns_2

        # Создаем DataFrame из list_ready_ty_excel с заданными колонками
        try:
            df = pd.DataFrame(self.list_ready_ty_excel, columns=all_columns)
            df = df.fillna('')  # Заполняем пустые значения, чтобы избежать ошибок при записи в Excel
        except Exception as e:
            create_error(
                name='CreatePriceExcel.write_to_excel',
                path=os.path.abspath(__file__),
                error=e
            )

            return

        # Создаем буфер для временного хранения файла
        output_buffer = io.BytesIO()

        try:
            # Пишем DataFrame в буфер
            with pd.ExcelWriter(output_buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name=self.custom_price_name, index=False)
            output_buffer.seek(0)  # Перемещаем указатель в начало буфера

            # Создаем или получаем объект ZaekPrice
            zaek_price, created = ZaekPrice.objects.get_or_create(
                name=self.custom_price_name,
                defaults={'created_at': timezone.now()}
            )

            # Проверяем наличие старого файла, и если есть - удаляем его
            if zaek_price.file:
                zaek_price.file.delete(save=False)  # Удаляем старый файл, если он существует

            # Сохраняем новый файл в поле 'file' модели ZaekPrice
            file_content = ContentFile(output_buffer.getvalue())
            zaek_price.file.save(f"{self.custom_price_name}.xlsx", file_content, save=False)

            # Сохраняем объект с новым файлом
            zaek_price.save()

        except Exception as e:
            create_error(
                name = 'CreatePriceExcel.write_to_excel',
                path = os.path.abspath(__file__),
                error = e
            )





def need_price_func():

    try:
        price = ZaekPrice.objects.get(name=custom_price_name)
    except :

        try:

            cl = CreatePriceExcel()
            price =cl.get_product_all()
        except Exception as e:

            create_error(
                name = 'need_price_func',
                path = os.path.abspath(__file__),
                error = e
            )
            price =None
    return price , custom_price_name