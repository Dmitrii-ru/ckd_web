import os

from django.db import transaction
from main.forms import validate_columns_df
from main.models import *
import openpyxl
import pandas as pd
import opcode
import zipfile
import xml.etree.ElementTree as ET
from django.db import transaction

from main.unils.parser_magadel.const import sheet_name, const, parent_split


def open_df(new_path):
    header = validate_columns_df(
        list(const.values()),
        new_path,
        sheet_name
    )
    excel_data_df = pd.read_excel(new_path, header=header, sheet_name=sheet_name, engine='openpyxl')
    import numpy as np
    excel_data_df = excel_data_df.replace({np.nan: None})
    return excel_data_df, header


def get_name_lvl(outline_level, row):
    try:
        return row[f'Unnamed: {outline_level}']
    except KeyError:
        return False


def clean_parent_dict(parent_dict, outline_level, name_lvl):
    '''
    Убираю уровни ниже текущего
    '''

    cleaned_dict = {key: value for key, value in parent_dict.items() if key <= outline_level}
    cleaned_dict[outline_level] = name_lvl

    return cleaned_dict


def get_parent(db_parens_dict, parent_dict):
    """
    Получаем словарь групп
    Проверяем  наличие группы
    Отдаем родителя(группу), обновлен словарь групп
    """

    parent_name = f"{parent_split}".join(parent_dict.values())
    parent_on_db = db_parens_dict.get(parent_name, None)

    if not parent_on_db:
        parent_on_db = GroupProductDKCMagadel.objects.create(name=parent_name)
        db_parens_dict[parent_name] = parent_on_db

    return db_parens_dict, parent_on_db


def get_columns_possible_deliveries(columns):
    '''
    Получаем колонки с датами
    '''
    columns_list = []
    for column in columns:
        try:
            pd.to_datetime(column)
            columns_list.append(column)
        except ValueError:
            pass
    return columns_list


def check_float(x):
    try:
        return float(x)
    except:
        return 0


def possible_deliveries_fanc(columns_possible_deliveries, row):
    '''
    Получаем общий список дат, где есть значение
    '''

    summ = 0
    list_possible_deliveries_date = ''
    for i in columns_possible_deliveries:
        try:
            value = row.get(i, None)
            if value:
                summ += check_float(value)
                if list_possible_deliveries_date:
                    list_possible_deliveries_date += f', {i} - {value}'
                else:
                    list_possible_deliveries_date = f'{i} - {value}'

        except:
            return '', 0
    return list_possible_deliveries_date, summ


from django.core.files.storage import default_storage


def delete_file(file_instance):
    try:
        file_path = file_instance.file.name


        if default_storage.exists(file_path):
            default_storage.delete(file_path)

        file_instance.delete()
    except Exception as e:
        print(f'Error deleting file: {e}')



def parser_maga_file_func(file_id):
    try:
        file_instance = FileMaga.objects.get(id=file_id)
        file_ = file_instance.file  # Это объект FieldFile
        file_path = file_.path  # Путь к файлу
        file_name = file_.name

        with transaction.atomic():
            df, header = open_df(file_path)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                with zip_ref.open('xl/worksheets/sheet1.xml') as sheet_file:
                    sheet_tree = ET.parse(sheet_file)
                    sheet_root = sheet_tree.getroot()
                    schema_rows = sheet_root.findall(
                        './/{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row')

                    parent_dict = {}
                    len_df = int(len(df))
                    count = 0

                    db_products_dict = {obj.code: obj for obj in ProductDKCMagadel.objects.all()}
                    db_parens_dict = {obj.name: obj for obj in GroupProductDKCMagadel.objects.all()}

                    list_product_to_create = []
                    list_product_to_update = []

                    const_code = const['Код']
                    const_free_balance = const['Свободный остаток']
                    const_about = const['Описание']
                    const_unit = const['ЕдИзм']
                    const_price = const['Цена без НДС, руб']

                    columns_possible_deliveries = get_columns_possible_deliveries(df.columns)

                    for schema_row in schema_rows[header + 1:]:
                        count += 1
                        outline_level = int(schema_row.get('outlineLevel', 0))
                        row_number = int(schema_row.get('r')) - header - 2
                        if row_number < len_df:
                            row = df.iloc[row_number]
                            name_lvl = get_name_lvl(outline_level, row)
                            if name_lvl:
                                parent_dict = clean_parent_dict(parent_dict, outline_level, name_lvl)

                            code = row.get(const_code, None)
                            if code:

                                db_parens_dict, parent = get_parent(db_parens_dict, parent_dict)
                                product = db_products_dict.get(code, None)

                                possible_deliveries, possible_deliveries_sum = possible_deliveries_fanc(
                                    columns_possible_deliveries, row
                                )

                                fb = check_float(row.get(const_free_balance, 0))
                                name = row.get(const_about, 'Описания нет')
                                unit = row.get(const_unit, 'Не указано')
                                price = check_float(row.get(const_price, 0))

                                if product:
                                    product.name = name
                                    product.parent = parent
                                    product.free_balance = fb
                                    product.list_possible_deliveries = possible_deliveries
                                    product.sum_possible_deliveries = possible_deliveries_sum
                                    product.unin = unit
                                    product.price = price

                                    list_product_to_update.append(product)

                                else:

                                    new_product = ProductDKCMagadel(
                                        code=code,
                                        name=name,
                                        parent=parent,
                                        list_possible_deliveries=possible_deliveries,
                                        sum_possible_deliveries=possible_deliveries_sum,
                                        free_balance=fb,
                                        unit=unit,
                                        price=price,
                                    )

                                    list_product_to_create.append(new_product)

                    if list_product_to_update:
                        ProductDKCMagadel.objects.bulk_update(list_product_to_update, [
                            'name',
                            'parent',
                            'free_balance',
                            'list_possible_deliveries',
                            'sum_possible_deliveries',
                            'unit',
                            'price',
                        ], batch_size=100)

                    if list_product_to_create:
                        ProductDKCMagadel.objects.bulk_create(list_product_to_create, batch_size=100)

                    maga = Magadel.objects.first()
                    if maga:
                        maga.name = file_name
                    else:
                        maga = Magadel(name=file_name)
                    maga.save()
                    delete_file(file_instance)
    except Exception as e:

        return f" Ошибка загрузки файла {e}"
