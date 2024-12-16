import os

import pandas as pd
from zaek.models import ClassificationPriceProduct
from base_app.utils.errors_plase import create_error
from zaek.consts_zaek import exception_values, extra_values, delimiter_price_csv, price_groups, classification_str




def get_classifications_ppo(classification,classifications_objects):
    classification_obj_on_db = classifications_objects.get(classification,None)
    if not classification_obj_on_db:
        classification_obj_on_db = ClassificationPriceProduct.objects.create(
            name=classification
        )
        classifications_objects[classification] = classification_obj_on_db
    return classification_obj_on_db


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

        classifications_objects = {
            obj.name: obj for obj in ClassificationPriceProduct.objects.all()
        }

        for i ,row in df.iterrows():
            if row['Артикул']:
                art = str(row['Артикул'])
                price_group_2 = str(row['Ценовая группа']).replace('"','')
                summary_price_group = row['Ценовая группа сводная']
                classification = row[classification_str]

                if any(exception_value in price_group_2 for exception_value in exception_values):
                    str_exception_values = ', '.join(exception_values)
                    classification = f'ПП КЭАЗ исключение {str_exception_values}'

                if classification == 'ПП KEAZ Optima':
                    sale = int(row.get('Скидка по договору,%',0))
                    if 39 < sale <41:
                        classification = 'ПП KEAZ Optima Проектный'

                dict_product_groups[art] = {
                    'Ценовая группа': price_group_2,
                    'Ценовая группа сводная': summary_price_group,
                    f'{classification_str}': get_classifications_ppo(classification,classifications_objects)
                }


        return dict_product_groups

    except Exception as e:
        create_error(
            name='parser_price_dist',
            path=os.path.abspath(__file__),
            error=e
        )



