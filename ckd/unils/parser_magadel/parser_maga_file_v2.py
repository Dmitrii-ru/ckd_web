import os
from django.db import transaction
from ckd.forms import validate_columns_df
from ckd.models import *
import openpyxl
import pandas as pd
import zipfile
import xml.etree.ElementTree as ET
from django.core.files.storage import default_storage
from ckd.unils.parser_magadel.const import sheet_name, const, parent_split


class MagaFileParser:

    def __init__(self, file_id):
        self.file_instance = FileMaga.objects.get(id=file_id)
        self.file_ = self.file_instance.file
        self.file_path = self.file_.path
        self.file_name = self.file_.name
        self.df = None
        self.header = None
        self.len_df = None
        self.consts = {}
        self.columns_possible_deliveries = []
        self.parent_dict = {}
        self.db_products_dict = {}
        self.db_parens_dict = {}
        self.list_product_to_create = []
        self.list_product_to_update = []

    def open_df(self):
        header = validate_columns_df(list(const.values()), self.file_path, sheet_name)
        excel_data_df = pd.read_excel(self.file_path, header=header, sheet_name=sheet_name, engine='openpyxl')
        # excel_data_df = excel_data_df.replace({pd.NA: None})
        self.df = excel_data_df
        self.header = header
        self.len_df = len(excel_data_df)

    def get_name_lvl(self, outline_level, row):
        try:
            return row[f'Unnamed: {outline_level}']
        except KeyError:
            return False

    def clean_parent_dict(self, parent_dict, outline_level, name_lvl):
        cleaned_dict = {key: value for key, value in parent_dict.items() if key <= outline_level}
        cleaned_dict[outline_level] = name_lvl
        return cleaned_dict

    def get_parent(self, db_parens_dict, parent_dict):
        parent_name = f"{parent_split}".join(parent_dict.values())
        parent_on_db = db_parens_dict.get(parent_name, None)

        if not parent_on_db:
            parent_on_db = GroupProductDKCMagadel.objects.create(name=parent_name)
            db_parens_dict[parent_name] = parent_on_db
        print(parent_on_db)
        return db_parens_dict, parent_on_db

    def get_columns_possible_deliveries(self, columns):
        columns_list = []
        for column in columns:
            try:
                pd.to_datetime(column)
                columns_list.append(column)
            except ValueError:
                pass
        return columns_list

    def check_float(self, x):
        try:
            return float(x)
        except:
            return 0

    def possible_deliveries_fanc(self, columns_possible_deliveries, row):
        summ = 0
        list_possible_deliveries_date = ''
        for i in columns_possible_deliveries:
            try:
                value = row.get(i, None)
                if value:
                    summ += self.check_float(value)
                    if list_possible_deliveries_date:
                        list_possible_deliveries_date += f', {i} - {value}'
                    else:
                        list_possible_deliveries_date = f'{i} - {value}'
            except:
                return '', 0
        return list_possible_deliveries_date, summ

    def delete_file(self):
        try:
            file_path = self.file_instance.file.name
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
            self.file_instance.delete()
        except Exception as e:
            print(f'Error deleting file: {e}')

    # def process_row(self, row):
    #     outline_level = int(row.get('outlineLevel', 0))
    #     row_number = int(row.get('r')) - self.consts['header'] - 2
    #     print(outline_level)

        # if row_number < self.len_df:
        #     df_row = self.df.iloc[row_number]
        #     name_lvl = self.get_name_lvl(outline_level, df_row)
        #     if name_lvl:
        #         self.parent_dict = self.clean_parent_dict(self.parent_dict, outline_level, name_lvl)
        #
        #     code = df_row.get(self.consts['code'], None)
        #     if code:
        #         self.db_parens_dict, parent = self.get_parent(self.db_parens_dict, self.parent_dict)
        #         product = self.db_products_dict.get(code, None)
        #
        #         possible_deliveries, possible_deliveries_sum = self.possible_deliveries_fanc(
        #             self.columns_possible_deliveries, df_row
        #         )
        #
        #         fb = self.check_float(df_row.get(self.consts['free_balance'], 0))
        #         name = df_row.get(self.consts['about'], 'Описания нет')
        #         unit = df_row.get(self.consts['unit'], 'Не указано')
        #         price = self.check_float(df_row.get(self.consts['price'], 0))
        #
        #         if product:
        #             product.name = name
        #             product.parent = parent
        #             product.free_balance = fb
        #             product.list_possible_deliveries = possible_deliveries
        #             product.sum_possible_deliveries = possible_deliveries_sum
        #             product.unit = unit
        #             product.price = price
        #             return 'update', product
        #         else:
        #             new_product = ProductDKCMagadel(
        #                 code=code,
        #                 name=name,
        #                 parent=parent,
        #                 list_possible_deliveries=possible_deliveries,
        #                 sum_possible_deliveries=possible_deliveries_sum,
        #                 free_balance=fb,
        #                 unit=unit,
        #                 price=price,
        #             )
        #             return 'create', new_product
        #
        # return None, None

    def prepare_parsing(self):
        self.open_df()
        for i,row in self.df.iter():
            print(i,row)

        self.consts = {
            'header': self.header,
            'code': const['Код'],
            'free_balance': const['Свободный остаток'],
            'about': const['Описание'],
            'unit': const['ЕдИзм'],
            'price': const['Цена без НДС, руб'],
        }
        self.columns_possible_deliveries = self.get_columns_possible_deliveries(self.df.columns)
        self.db_products_dict = {obj.code: obj for obj in ProductDKCMagadel.objects.all()}
        self.db_parens_dict = {obj.name: obj for obj in GroupProductDKCMagadel.objects.all()}

    def parse(self):
        self.prepare_parsing()
        # with transaction.atomic():
        #     with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
        #         with zip_ref.open('xl/worksheets/sheet1.xml') as sheet_file:
        #             for event, elem in ET.iterparse(sheet_file, events=('start', 'end')):
        #                 if event == 'end' and elem.tag.endswith('row'):
        #                     print(elem)
        #                     action, product = self.process_row(elem)
        #                     if action == 'update':
        #                         self.list_product_to_update.append(product)
        #                     elif action == 'create':
        #                         self.list_product_to_create.append(product)
        #                     elem.clear()  # Освобождение памяти после обработки элемента
        #
        #     self.save_products()
        #
        #     maga = Magadel.objects.first()
        #     if maga:
        #         maga.name = self.file_name
        #     else:
        #         maga = Magadel(name=self.file_name)
        #     maga.save()
        #     self.delete_file()


    def save_products(self):
        if self.list_product_to_update:
            ProductDKCMagadel.objects.bulk_update(self.list_product_to_update, [
                'name',
                'parent',
                'free_balance',
                'list_possible_deliveries',
                'sum_possible_deliveries',
                'unit',
                'price',
            ], batch_size=100)

        if self.list_product_to_create:
            ProductDKCMagadel.objects.bulk_create(self.list_product_to_create, batch_size=100)


def parser_maga_file_func(file_id):
    try:
        parser = MagaFileParser(file_id)
        parser.parse()
    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")
        return f"Ошибка загрузки файла: {e}"