import os
import openpyxl
from zaek.models import Product
from zaek.utils.parser_price.consts_zaek import attrs_update_products, split_parent_base, split_parent_obj
import pandas as pd

# def get_object_attrs(objects_model):
#     objects_list = []
#
#
#     for attr in attrs_update:
#
#         value = getattr(objects_model, attr, None)
#         key = objects_model._meta.get_field(f'{attr}').verbose_name
#
#
#
#
#
#
#
# def need_price_func():
#     objects_all = Product.objects.all()
#
#     columns = [] + attrs_update
#
#
#
#     df = pd.DataFrame(columns=columns)
#
#
#     df.to_excel("output.xlsx", index=False)
#     print("Файл 'output.xlsx' создан с колонками:", columns)
#
#     for obj in objects_all:
#         get_object_attrs(obj)
#     return




class CreatePriceExcel:

    def __init__(
            self,
            model = Product,
            attrs_update = attrs_update_products

    ):
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

    def write_to_excel(self, output_file="1.xlsx", sheet_name="Sheet1"):
        if not output_file.endswith(".xlsx"):
            output_file += ".xlsx"
        sorted_columns = [self.level_columns[key] for key in sorted(self.level_columns.keys())]
        all_columns = self.columns_1 + sorted_columns + self.columns_2
        df = pd.DataFrame(self.list_ready_ty_excel, columns=all_columns)
        df = df.fillna('')
        try:
            if os.path.exists(output_file):
                os.remove(output_file)
            with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"Файл '{output_file}' успешно создан на листе '{sheet_name}'")
        except Exception as e:
            print("Ошибка записи в Excel:", e)
