from operator import itemgetter
from datetime import datetime
import openpyxl
import zipfile
import xml.etree.ElementTree as ET
import pandas as pd
from main.forms import validate_columns_df
from main.models import GroupProductDKCMagadel, ProductDKCMagadel, Magadel
from main.unils.parser_magadel.const import sheet_name, const, parent_split
from main.unils.parser_magadel.parser_maga_file import get_parent


class ExcelParser:
    def __init__(self, maga):
        self.maga = maga
        self.file_path = maga.file
        self.parent_dict = {}
        self.DB_parents_dict = {obj.name: obj for obj in GroupProductDKCMagadel.objects.all()}
        self.parent = None
        self.columns_possible_deliveries = None
        self.DB_products_dict= {obj.code: obj for obj in ProductDKCMagadel.objects.all()}
        self.list_product_to_update=[]
        self.list_product_to_create=[]

    def clean_parent_dict(self, outline_level, name_lvl):
        '''
        Убираю уровни ниже текущего
        '''

        self.parent_dict = {key: value for key, value in self.parent_dict.items() if key <= outline_level }
        self.parent_dict[outline_level] = name_lvl


    def upload_parent_dict(self,row):
        for outline_level,name_lvl in enumerate(row):
            if name_lvl:
                self.clean_parent_dict(outline_level,name_lvl)


    def get_parent(self):
        """
        Получаем словарь групп
        Проверяем  наличие группы
        Отдаем родителя(группу), обновлен словарь групп
        """

        parent_name = f"{parent_split}".join(self.parent_dict.values())
        parent_on_db = self.DB_parents_dict.get(parent_name, None)

        if not parent_on_db:
            parent_on_db = GroupProductDKCMagadel.objects.create(name=parent_name)
            self.DB_parents_dict[parent_name] = parent_on_db
        return parent_on_db

    @staticmethod
    def check_float(x):
        try:
            return float(x)
        except:
            return 0

    def possible_deliveries_fanc(self, row):
        '''
        Получаем общий список дат, где есть значение
        '''

        summ = 0
        list_possible_deliveries_date = ''
        for i in self.columns_possible_deliveries:
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

    def get_columns_possible_deliveries(self,columns):
        '''
        Получаем колонки с датами
        '''
        columns_list = []
        for column in columns:
            if column is not None:  # Проверяем, что column не None
                try:
                    # Попробуем преобразовать строку в дату
                    datetime.strptime(column, '%d.%m.%Y')
                    columns_list.append(column)
                except ValueError:
                    # Если возникла ошибка, значит это не дата
                    pass
        self.columns_possible_deliveries = columns_list

    def delete_file(self,file_instance):
        from django.core.files.storage import default_storage
        try:
            file_path = file_instance.file.name

            if default_storage.exists(file_path):
                default_storage.delete(file_path)

            file_instance.delete()
        except Exception as e:
            print(f'Error deleting file: {e}')

    def parse(self):
        header = validate_columns_df(list(const.values()), self.file_path, sheet_name)
        workbook = openpyxl.load_workbook(self.file_path, read_only=True)
        sheet = workbook.active
        column_names = [cell.value for cell in sheet[header+1]]
        self.get_columns_possible_deliveries(column_names)

        const_free_balance = const['Свободный остаток']
        const_about = const['Описание']
        const_unit = const['ЕдИзм']
        const_price = const['Цена без НДС, руб']

        for row in sheet.iter_rows(min_row=header+2, values_only=True):
            row_data = dict(zip(column_names, row))
            kode = row_data.get(const['Код'], None)
            product = self.DB_products_dict.get(kode, None)

            if not kode:
                self.upload_parent_dict(row)

            else:
                possible_deliveries, possible_deliveries_sum = self.possible_deliveries_fanc(row_data)
                fb = self.check_float(row_data.get(const_free_balance, 0))
                name = row_data.get(const_about, 'Описания нет')
                unit = row_data.get(const_unit, 'Не указано')
                price = self.check_float(row_data.get(const_price, 0))
                parent = self.get_parent()

                if product:
                    product.name = name
                    product.parent = parent
                    product.free_balance = fb
                    product.list_possible_deliveries = possible_deliveries
                    product.sum_possible_deliveries = possible_deliveries_sum
                    product.unin = unit
                    product.price = price

                    self.list_product_to_update.append(product)

                else:

                    new_product = ProductDKCMagadel(
                        code=kode,
                        name=name,
                        parent=parent,
                        list_possible_deliveries=possible_deliveries,
                        sum_possible_deliveries=possible_deliveries_sum,
                        free_balance=fb,
                        unit=unit,
                        price=price,
                    )

                    self.list_product_to_create.append(new_product)
        print('save')

        chunk_size = 1000

        if self.list_product_to_update:
            for i in range(0, len(self.list_product_to_update), chunk_size):
                chunk = self.list_product_to_update[i:i + chunk_size]

                ProductDKCMagadel.objects.bulk_update(chunk, [
                    'name',
                    'parent',
                    'free_balance',
                    'list_possible_deliveries',
                    'sum_possible_deliveries',
                    'unit',
                    'price',
                ], batch_size=chunk_size)

        if self.list_product_to_create:
            for i in range(0, len(self.list_product_to_create), chunk_size):
                chunk = self.list_product_to_create[i:i + chunk_size]
                ProductDKCMagadel.objects.bulk_create(chunk, batch_size=chunk_size)



        # if self.list_product_to_update:
        #     ProductDKCMagadel.objects.bulk_update(self.list_product_to_update, [
        #             'name',
        #             'parent',
        #             'free_balance',
        #             'list_possible_deliveries',
        #             'sum_possible_deliveries',
        #             'unit',
        #             'price',
        #         ], batch_size=1000)
        #
        # if self.list_product_to_create:
        #     ProductDKCMagadel.objects.bulk_create(self.list_product_to_create, batch_size=1000)




        db_maga = Magadel.objects.first()

        try:
            file_name =str(self.maga.file.name).replace('files/','')
        except KeyError:
            file_name =str(self.maga.file.name)

        if db_maga:
            db_maga.name = file_name
        else:
            db_maga = Magadel(name=file_name)
        db_maga.save()
        self.delete_file(self.maga)
        print('end')


