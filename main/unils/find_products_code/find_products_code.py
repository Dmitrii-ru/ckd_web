import os
from io import BytesIO

from core_app.redis_cli import RedisClientMain
from main.forms import validate_columns_df
from main.models import *
import openpyxl
import pandas as pd
from main.unils.parser_magadel.const import parent_split
from main.unils.find_products_code.const import sheet_name, const_columns


def open_df(new_path):
    header = validate_columns_df(
        list(const_columns.values()),
        new_path,
        sheet_name
    )
    excel_data_df = pd.read_excel(new_path, header=header, sheet_name=sheet_name, engine='openpyxl')
    import numpy as np
    excel_data_df = excel_data_df.replace({np.nan: None})
    return excel_data_df, header


def create_df_columns(df, column):
    """
    Создаем колонку если ее нет
    """

    if isinstance(column, (list, tuple)):
        for col in column:
            if col not in df.columns:
                df[col] = None

    elif isinstance(column, str):
        if column not in df.columns:
            df[column] = None


def get_level_groups(level_group_columns_name, group, df, i):
    """
    Добавляем в level_group_columns_name название колонок
    И проверим на наличие колонок в дф
    """
    for index, value in enumerate(group.split(parent_split)):
        column = f'Уровень - {index}'
        if column not in level_group_columns_name:
            level_group_columns_name.append(column)
            create_df_columns(df, column)
        df.at[i, column] = value


def get_float(x):
    try:
        return float(x)
    except:
        return 0


def update_values_object(object, df, index_row, quantity):
    free_balance = object.get('free_balance', 0)
    sum_possible_deliveries = object.get('sum_possible_deliveries', 0)
    list_possible_deliveries = object.get('list_possible_deliveries', 'Нет значения')
    unit = object.get('unit', 'Нет значения')
    request_quantity = get_float(quantity)
    sum_possible_deliveries_free_balance = (sum_possible_deliveries + free_balance) - request_quantity
    name = object.get('name', 'Нет значения')

    df.at[index_row, 'Свободный остаток'] = free_balance
    df.at[index_row, 'Свободный остаток - Кол'] = free_balance - request_quantity
    df.at[index_row, 'Свободные поступления'] = sum_possible_deliveries
    df.at[index_row, 'Свободный остаток - Свободные поступления- Кол'] = sum_possible_deliveries_free_balance
    df.at[index_row, 'Информация о поступлениях'] = list_possible_deliveries
    df.at[index_row, 'Описание'] = name
    df.at[index_row, 'ЕдИзм'] = unit


def find_products(file):
    df, header = open_df(file)
    rm = RedisClientMain()
    products, groups = rm.get_products_parents(model_product=ProductDKCMagadel, model_group=GroupProductDKCMagadel)

    base_columns = (list(const_columns.values()))

    new_columns = [
        'Свободный остаток',
        'Свободный остаток - Кол',
        'Свободные поступления',
        'Свободный остаток - Свободные поступления- Кол',
        'Информация о поступлениях',
        'Описание',
        'ЕдИзм',
    ]

    create_df_columns(df, new_columns)

    level_group_columns_name = []

    for index_row, row in df.iterrows():
        product_code = row.get('Код')

        if product_code:
            product = products.get(product_code)
            if product:
                quantity = row.get('Кол')
                update_values_object(product, df, index_row, quantity)
                group = product.get('parent')
                if group:
                    get_level_groups(level_group_columns_name, group, df, index_row)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    return output, file.name


def find_products_code_func(file):
    new_df = find_products(file)
    return new_df
