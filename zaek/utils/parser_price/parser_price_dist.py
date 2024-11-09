

import pandas as pd

from zaek.utils.parser_price.consts_zaek import exception_values, extra_values

file_path = '/home/dima/Python/django/ckd_web/zaek/utils/parser_price/628607_utf8.csv'

def parser_price_dist():
    df = pd.read_csv(file_path, delimiter=';', encoding='utf8')
    dict_product_groups ={}
    for i ,row in df.iterrows():
        if row['Артикул']:
            art = str(row['Артикул'])
            price_group_2 = str(row['Ценовая группа']).replace('"','')
            summary_price_group = row['Ценовая группа сводная']
            classification = row['Классификация ПП']
            if any(exception_value in price_group_2 for exception_value in exception_values):
                if not any(extra_value in price_group_2 for extra_value in extra_values):
                    str_exception_values = ', '.join(exception_values)
                    classification = f'ПП КЭАЗ исключение {str_exception_values}'
            dict_product_groups[art] = {
                'Ценовая группа': price_group_2,
                'Ценовая группа сводная': summary_price_group,
                'Классификация ПП': classification
            }
    return dict_product_groups



