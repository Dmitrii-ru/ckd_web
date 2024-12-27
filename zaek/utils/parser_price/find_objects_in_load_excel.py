# from decimal import Decimal
# from io import BytesIO
#
# from django.db.models import Prefetch
# from redis.commands.search.reducers import count
# from openpyxl.styles import PatternFill
# from zaek.consts_zaek import split_parent_base, split_parent_obj
# from zaek.models import Product, ClientClassificationDiscount, VolumeAtDiscount, ClassificationPriceProduct
# from openpyxl import Workbook
# from openpyxl.utils import get_column_letter
#
# import pandas as pd
#
# class CreateDictFindObjectsExcel:
#     def __init__(
#             self,
#             request_products=None,
#             request_products_dict=None
#     ):
#
#         self.request_products = request_products
#         self.request_products_dict = request_products_dict
#         self.products = {}
#         self.price_group_list_columns_to_sort=[]
#         self.classification_columns_to_sort = []
#         self.product = {}
#         self.total_price_not_nds = 0
#         self.total_price_with_nds = 0
#         self.base_header = {
#             'Артикул':'Артикул',
#             'Цена (без НДС) руб.':'Цена (без НДС) руб.',
#             'Цена (с НДС) руб.':'Цена (с НДС) руб.',
#             'Классификация ПП':'Классификация ПП',
#             'Кол-во':'Кол-во'
#         }
#         self.test_header = {}
#
#         self.wb = Workbook()
#         self.ws = self.wb.active
#         self.start_header = 2
#         self.ROC = 48
#
#     def get_price_group_list(self,price_group_list):
#         """Добавляем уровни родителей в объект"""
#         for group in price_group_list.split(split_parent_base):
#             level_value = group.split(split_parent_obj)
#             level = int(level_value[0])
#             value = level_value[1]
#             level_name = f'Уровень: {level}'
#             if level_name not in self.price_group_list_columns_to_sort:
#                 self.price_group_list_columns_to_sort.append(level_name)
#             self.product[f'Уровень: {level}'] = value
#
#     def get_float(self,obj):
#
#         try:
#             float_obj = float(obj)
#             if float_obj<0:
#                 return 0.0
#             else:
#                 return float_obj
#         except:
#             return 0.0
#
#
#     def get_or_create_header(self,key):
#         obj = self.test_header.get(key)
#         if obj:
#             return obj
#         col_letter =get_column_letter(len(self.test_header)+1)
#         self.test_header[key] = col_letter
#         self.ws[f"{col_letter}{self.start_header}"] = key
#         return col_letter
#
#
#     def create_dict(self):
#
#         """Формируем объект в виде словаря"""
#         list_request_products_dict_keys= list(self.request_products_dict.keys())
#         print(list_request_products_dict_keys)
#         print(list_request_products_dict_keys)
#         count_request_products = len(list_request_products_dict_keys)
#         dict_request_products = {obj.art: obj for obj in self.request_products}
#         list_type_client = []
#
#         col_letter_art = None
#         col_letter_price_with_nds = None
#         col_letter_kol = None
#         col_letter_summ_base = None
#         col_letter_classification = None
#         col_letter_type_client = None
#
#         for  idx , art_obj in enumerate(list_request_products_dict_keys,start=self.start_header + 1):
#             request_product = dict_request_products.get(art_obj)
#             print(request_product)
#             if request_product:
#                 col_letter_art = self.get_or_create_header('Артикул')
#                 self.ws[f'{col_letter_art}{idx}'] = request_product.art
#
#                 col_letter_classification = self.get_or_create_header('Номенклатура')
#                 self.ws[f'{col_letter_classification}{idx}'] = request_product.name
#
#                 col_letter_kol = self.get_or_create_header('Кол-во')
#                 count_product = Decimal(self.get_float(self.request_products_dict[request_product.art]))
#                 self.ws[f'{col_letter_kol}{idx}'] = count_product
#
#                 col_letter_classification = self.get_or_create_header('Классификация ПП')
#                 self.ws[f'{col_letter_classification}{idx}'] = request_product.classification.name
#
#                 col_letter_price_with_nds = self.get_or_create_header('Цена (с НДС) руб.')
#                 self.ws[f'{col_letter_price_with_nds}{idx}'] = request_product.price_with_nds
#
#
#
#
#                 col_letter_summ_base = self.get_or_create_header('Сумма по прайсу с НДС')
#                 self.ws[f'{col_letter_summ_base}{idx}'] = \
#                     f"={col_letter_price_with_nds}{idx} * {col_letter_kol}{idx}"
#
#
#
#
#                 for discount in request_product.classification.classification_discounts.all():
#                     discount_type_client_type = discount.type_client.type
#                     list_type_client.append(f'{discount_type_client_type}')
#                     col_letter_type_client_discount = self.get_or_create_header(f'{discount_type_client_type} скидка')
#                     col_letter_type_client_sale_solo = self.get_or_create_header(f'{discount_type_client_type} шт с НДС')
#                     col_letter_type_client_sale_summ = self.get_or_create_header(f'{discount_type_client_type} сумма с НДС')
#
#                     self.ws[f'{col_letter_type_client_discount}{idx}'] = discount.discount
#
#                     self.ws[f'{col_letter_type_client_sale_solo}{idx}'] = (
#                         f'={col_letter_price_with_nds}{idx}*(1-{col_letter_type_client_discount}{idx}/100)'
#                     )
#                     self.ws[f'{col_letter_type_client_sale_summ}{idx}'] = (
#                         f'={col_letter_kol}{idx}*{col_letter_type_client_sale_solo}{idx}'
#                     )
#
#
#
#             else:
#                 col_letter_art = self.get_or_create_header('Артикул')
#                 self.ws[f'{col_letter_art}{idx}'] = art_obj
#
#
#
#         start_row = self.start_header + 1  # Начальная строка данных
#         end_row = self.start_header + count_request_products  # Конечная строка данных
#
#
#         formula = f"=SUM({col_letter_summ_base}{start_row}:{col_letter_summ_base}{end_row})"
#         self.ws[f'{col_letter_summ_base}{end_row+1}'] = formula
#
#
#
#         for type_client in list_type_client:
#             col_letter_client = self.get_or_create_header(f'{type_client} сумма с НДС')
#             formula = f"=SUM({col_letter_client}{start_row}:{col_letter_client}{end_row})"
#             self.ws[f'{col_letter_client}{end_row+1}'] = formula
#
#         # self.wb.save("/home/dima/Python/django/ckd_web/zaek/utils/parser_price/v.xlsx")
#         self.wb.save("/home/dima/Python/django/ckd_web/zaek/utils/parser_price/v.xlsx")
#
#
#
#
#         return self.wb
#
#
#
# def find_objects_in_load_excel(file=None):
#
#         pd.read_excel(file)
#         data_dict = {}
#         for i , row in pd.read_excel(file).iterrows():
#             art = str(row['Арт'])
#             data_dict[art] = row['Кол']
#
#
#         data_keys_list = list(data_dict.keys())
#
#         products = Product.objects.prefetch_related(
#             'classification',
#                 Prefetch(
#                     'classification__classification_discounts',  # Скидки, связанные через ClassificationPriceProduct
#                     queryset=ClientClassificationDiscount.objects.select_related(
#                         'type_client',
#                         'classification_price_product',
#                     )
#                 ),
#
#             Prefetch(
#                 'classification__classification_volume_discounts',  # Скидки за объем, связанные через ClassificationPriceProduct
#                 queryset=VolumeAtDiscount.objects.select_related('volume_level', 'type_client'),
#             )
#         ).filter(art__in=data_keys_list)
#
#
#         print(products)
#         if products:
#
#             new_excel_file = CreateDictFindObjectsExcel
#             excel_creator = new_excel_file(
#                 request_products = products,
#                 request_products_dict = data_dict
#             ).create_dict()
#
#             print('______________________________________________________')
#             print(excel_creator,'wwww')
#
#             output = BytesIO()
#             excel_creator.save(output)
#             output.seek(0)
#
#
#             return output




from decimal import Decimal
from io import BytesIO

from django.db.models import Prefetch
from redis.commands.search.reducers import count
from openpyxl.styles import PatternFill
from zaek.consts_zaek import split_parent_base, split_parent_obj
from zaek.models import Product, ClientClassificationDiscount, VolumeAtDiscount, ClassificationPriceProduct
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

import pandas as pd

class CreateDictFindObjectsExcel:
    def __init__(
            self,
            request_products=None,
            request_products_dict=None,
            df = None
    ):
        self.request_products = request_products
        self.request_products_dict = request_products_dict
        self.df=df
        self.test_header = {}
        self.wb = Workbook()
        self.ws = self.wb.active
        self.start_header = 2
        self.ROC = 48

    def get_price_group_list(self,price_group_list):
        """Добавляем уровни родителей в объект"""
        for group in price_group_list.split(split_parent_base):
            level_value = group.split(split_parent_obj)
            level = int(level_value[0])
            value = level_value[1]
            level_name = f'Уровень: {level}'
            if level_name not in self.price_group_list_columns_to_sort:
                self.price_group_list_columns_to_sort.append(level_name)
            self.product[f'Уровень: {level}'] = value

    def get_float(self,obj):

        try:
            float_obj = float(obj)
            if float_obj<0:
                return 0.0
            else:
                return float_obj
        except:
            return 0.0


    def get_or_create_header(self,key):
        obj = self.test_header.get(key)
        if obj:
            return obj
        col_letter =get_column_letter(len(self.test_header)+1)
        self.test_header[key] = col_letter
        self.ws[f"{col_letter}{self.start_header-1}"] = key
        return col_letter


    def color_section(self,color_type_client_type):
        return PatternFill(start_color=color_type_client_type, end_color=color_type_client_type, fill_type="solid")

    def create_dict(self):

        """Формируем объект в виде словаря"""
        list_request_products_dict_keys= list(self.request_products_dict.keys())
        count_request_products = len(list_request_products_dict_keys)
        dict_request_products = {obj.art: obj for obj in self.request_products}
        list_type_client = []

        col_letter_art = None
        col_letter_price_with_nds = None
        col_letter_kol = None
        col_letter_summ_base = None
        col_letter_classification = None
        col_letter_type_client = None


        for i, row in self.df.iterrows():
            idx = i + self.start_header
            art_obj = str(row['Арт'])
            count_odj = row['Кол']

            request_product = dict_request_products.get(art_obj)
            if request_product:
                col_letter_art = self.get_or_create_header('Артикул')
                self.ws[f'{col_letter_art}{idx}'] = request_product.art

                col_letter_classification = self.get_or_create_header('Номенклатура')
                self.ws[f'{col_letter_classification}{idx}'] = request_product.name

                col_letter_kol = self.get_or_create_header('Кол-во')
                count_product = Decimal(self.get_float(count_odj))
                self.ws[f'{col_letter_kol}{idx}'] = count_product

                col_letter_classification = self.get_or_create_header('Классификация ПП')
                self.ws[f'{col_letter_classification}{idx}'] = request_product.classification.name

                col_letter_price_with_nds = self.get_or_create_header('Цена (с НДС) руб.')
                self.ws[f'{col_letter_price_with_nds}{idx}'] = request_product.price_with_nds

                col_letter_summ_base = self.get_or_create_header('Сумма по прайсу с НДС')
                self.ws[f'{col_letter_summ_base}{idx}'] = \
                    f"={col_letter_price_with_nds}{idx} * {col_letter_kol}{idx}"




                for discount in request_product.classification.classification_discounts.all():
                    discount_type_client_type = discount.type_client.type
                    color_type_client_type = discount.type_client.color
                    list_type_client.append(f'{discount_type_client_type}')

                    col_letter_type_client_discount = self.get_or_create_header(f'{discount_type_client_type} скидка')
                    col_letter_type_client_sale_solo = self.get_or_create_header(f'{discount_type_client_type} шт с НДС')
                    col_letter_type_client_sale_summ = self.get_or_create_header(f'{discount_type_client_type} сумма с НДС')


                    self.ws[f'{col_letter_type_client_discount}{idx}'] = discount.discount
                    self.ws[f'{col_letter_type_client_discount}{idx}'].fill = self.color_section(color_type_client_type)

                    self.ws[f'{col_letter_type_client_sale_solo}{idx}'] = (
                        f'={col_letter_price_with_nds}{idx}*(1-{col_letter_type_client_discount}{idx}/100)'
                    )
                    self.ws[f'{col_letter_type_client_sale_solo}{idx}'].fill = self.color_section(color_type_client_type)

                    self.ws[f'{col_letter_type_client_sale_summ}{idx}'] = (
                        f'={col_letter_kol}{idx}*{col_letter_type_client_sale_solo}{idx}'
                    )
                    self.ws[f'{col_letter_type_client_sale_summ}{idx}'].fill = self.color_section(color_type_client_type)



            else:
                col_letter_art = self.get_or_create_header('Артикул')
                self.ws[f'{col_letter_art}{idx}'] = art_obj



        start_row = self.start_header + 1  # Начальная строка данных
        end_row = self.start_header + count_request_products  # Конечная строка данных


        formula = f"=SUM({col_letter_summ_base}{start_row}:{col_letter_summ_base}{end_row})"
        self.ws[f'{col_letter_summ_base}{end_row+1}'] = formula



        for type_client in list_type_client:
            col_letter_client = self.get_or_create_header(f'{type_client} сумма с НДС')
            formula = f"=SUM({col_letter_client}{start_row}:{col_letter_client}{end_row})"
            self.ws[f'{col_letter_client}{end_row+1}'] = formula

        # self.wb.save("/home/dima/Python/django/ckd_web/zaek/utils/parser_price/v.xlsx")
        # self.wb.save("/home/dima/Python/django/ckd_web/zaek/utils/parser_price/v.xlsx")




        return self.wb



def find_objects_in_load_excel(file=None):

        pd.read_excel(file)
        data_dict = {}
        for i , row in pd.read_excel(file).iterrows():
            art = str(row['Арт'])
            data_dict[art] = row['Кол']


        data_keys_list = list(data_dict.keys())

        products = Product.objects.prefetch_related(
            'classification',
                Prefetch(
                    'classification__classification_discounts',  # Скидки, связанные через ClassificationPriceProduct
                    queryset=ClientClassificationDiscount.objects.select_related(
                        'type_client',
                        'classification_price_product',
                    )
                ),

            Prefetch(
                'classification__classification_volume_discounts',  # Скидки за объем, связанные через ClassificationPriceProduct
                queryset=VolumeAtDiscount.objects.select_related('volume_level', 'type_client'),
            )
        ).filter(art__in=data_keys_list)



        if products:

            new_excel_file = CreateDictFindObjectsExcel
            excel_creator = new_excel_file(
                request_products = products,
                request_products_dict = data_dict,
                df = pd.read_excel(file)
            ).create_dict()

            output = BytesIO()
            excel_creator.save(output)
            output.seek(0)
            return output

