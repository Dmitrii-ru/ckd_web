import os

import openpyxl
import pandas as pd
import opcode
import zipfile
import xml.etree.ElementTree as ET

sheet_name = 'Склад ДКС'
header = 6


def open_df(new_path):
    excel_data_df = pd.read_excel(new_path, header=header, sheet_name=sheet_name, engine='openpyxl')
    import numpy as np
    excel_data_df = excel_data_df.replace({np.nan: None})
    return excel_data_df


def get_name_lvl(outline_level, row):
    try:
        return row[f'Unnamed: {outline_level}']
    except KeyError:
        return False


def clean_parent_dict(parent_dict, outline_level):
    cleaned_dict = {key: value for key, value in parent_dict.items() if key <= outline_level}
    return cleaned_dict


def parser_maga_file_func(file):
    new_list_df = []
    with zipfile.ZipFile(file, 'r') as zip_ref:
        with zip_ref.open('xl/worksheets/sheet1.xml') as sheet_file:
            sheet_tree = ET.parse(sheet_file)
            sheet_root = sheet_tree.getroot()
            schema_rows = sheet_root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row')
            df = open_df(file)
            parent_dict = {}
            len_df = int(len(df))

            for schema_row in schema_rows[header + 1:]:
                outline_level = int(schema_row.get('outlineLevel', 0))
                row_number = int(schema_row.get('r')) - header - 2
                if row_number < len_df:
                    row = df.iloc[row_number]
                    name_lvl = get_name_lvl(outline_level, row)
                    if name_lvl:
                        parent_dict = clean_parent_dict(parent_dict, outline_level)
                        parent_dict[outline_level] = name_lvl
                    if row['Код']:
                        new_q = {
                            'Код': row['Код'],
                            'Описание': row['Описание']
                        }

                        for k, v in parent_dict.items():
                            new_q[f'Уровень {k}'] = v
                        new_list_df.append(new_q)
                        print(new_list_df)
