import os

import pandas as pd

from base_app.utils.errors_plase import create_error
from zaek.consts_zaek import exception_values, extra_values, delimiter_price_csv,price_groups



def parser_price_dist():
    import chardet
    from zaek.models import ZaekPrice

    try:
        price =  ZaekPrice.objects.get(name = price_groups)
        file_path = price.file.path

        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']

        df = pd.read_csv(file_path, delimiter=delimiter_price_csv, encoding=encoding)
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

    except Exception as e:
        create_error(
            name='parser_price_dist',
            path=os.path.abspath(__file__),
            error=e
        )



