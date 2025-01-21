import hashlib
import math
from decimal import Decimal
from io import BytesIO

from openpyxl.styles import PatternFill

from zaek.models import Product, ClassificationPriceProduct
import pandas as pd
from openpyxl import Workbook
from zaek.utils.parser_price.consolidated_table import create_dict_consolidated_table
from openpyxl.utils import get_column_letter, column_index_from_string


class PreDataLoadingInto:
    def __init__(
            self,
            excel ,
            slodnaya_bool
    ):
        self.close_df = excel
        self.slodnaya_bool = slodnaya_bool
        self.classification_pp = [obj.name for obj in ClassificationPriceProduct.objects.all()]
        self.wb = Workbook()
        self.ws = self.wb.active
        self.df_open = None
        self.list_object = []
        self.header_row = 1
        self.last_column = 0
        self.dict_classification_pp = {}
        self.dict_header = {}
        self.color_classification_pp= {}


    def pars_data_loading_into(self):
        self.df_open = pd.read_excel(self.close_df)
        self.list_object = set()

        if self.slodnaya_bool:
            cons = create_dict_consolidated_table(self.df_open)
            self.df_open = pd.DataFrame(list(cons.items()), columns=['Арт', 'Кол'])
            self.list_object = (list(cons.keys()))
        else:
            for i , row in self.df_open.iterrows():
               self.list_object.add(self.art_format(row['Арт']))

        self.create_dict_classification_pp_and_write_in_df()
        self.iter_data()

        return self.wb

    from openpyxl.styles import PatternFill

    def generate_color_from_number(self,number):
        value_str = str(number)

        value_hash = hashlib.md5(value_str.encode()).hexdigest()
        r = int(value_hash[:2], 16)
        g = int(value_hash[2:4], 16)
        b = int(value_hash[4:6], 16)
        return f"{r:02X}{g:02X}{b:02X}"



    def get_letter_column(self,key):
        value = self.dict_header.get(key)
        if value:
            return value
        col_letter = get_column_letter(len(self.dict_header)+1)
        self.dict_header[key]= col_letter

        self.ws[f"{col_letter}{self.header_row}"] = key
        return col_letter

    def color_section(self,color_type_client_type):
        """Настройки закраски клеток"""
        return PatternFill(start_color=color_type_client_type, end_color=color_type_client_type, fill_type="solid")

    def create_dict_classification_pp_and_write_in_df(self):
        for idx , value in enumerate(self.classification_pp,1):
            self.ws[f"A{idx}"] = value
            self.dict_classification_pp[value] = f'B{idx}'
            self.ws[f"B{idx}"] = 0
            self.header_row=idx

            color = self.generate_color_from_number(idx)
            self.color_classification_pp[value] = color
            self.ws[f"A{idx}"].fill = self.color_section(color)
            self.ws[f"B{idx}"].fill = self.color_section(color)


        self.ws[f"A{self.header_row + 1}"] = 'Конкурент'
        self.ws[f"B{self.header_row + 1}"] = 'Chint'
        self.dict_classification_pp['Конкурент'] = f'B{self.header_row + 1}'
        self.header_row+=3

    def get_float(self, obj):
        try:
            if isinstance(obj, Decimal):
                if obj.is_nan():
                    raise ValueError("Значение Decimal является NaN")
                float_obj = float(obj)

            else:
                float_obj = float(obj)
                if math.isnan(float_obj):
                    raise ValueError("Значение float является NaN")

            if float_obj < 0:
                ret = 0.0
            else:
                ret = float_obj

        except (ValueError, TypeError) as e:

            ret = 0.0
        return ret

    def art_format(self,art):
        try:
            return str(int(art))
        except:
            return str(art)

    def iter_data(self):
        products_filter = Product.objects.select_related('classification').filter(art__in=self.list_object)
        dict_products_filter = {obj.art: obj for obj in products_filter}
        l_row = self.header_row + 1

        letter_column_art = self.get_letter_column('Арт')
        letter_column_col = self.get_letter_column('Кол')
        letter_column_sale = self.get_letter_column('Скидка')
        letter_column_competitor =self.get_letter_column('Конкурент')
        letter_column_classification= self.get_letter_column('Классификация ПП')
        letter_column_name = self.get_letter_column('Наименование')

        for i, row in self.df_open.iterrows():
            row_num = l_row + i
            art = row['Арт']
            kol = self.get_float(row['Кол'])
            obj = dict_products_filter.get(art)

            if obj:
                self.ws[f"{letter_column_name}{row_num}"] = obj.name
                self.ws[f"{letter_column_art}{row_num}"] = obj.art
                self.ws[f"{letter_column_col}{row_num}"] = kol

                classification_letter_num = self.dict_classification_pp.get(
                    f'{obj.classification.name}',
                    'Нет данных'
                )


                self.ws[f"{letter_column_sale}{row_num}"] = f"={classification_letter_num}"
                comp_letter_num = self.dict_classification_pp.get('Конкурент', 'Нет данных')
                self.ws[f"{letter_column_competitor}{row_num}"] = f"={comp_letter_num}"
                self.ws[f"{letter_column_classification}{row_num}"] = obj.classification.name

                classification_color = self.color_classification_pp.get(obj.classification.name)
                if classification_color:
                    self.ws[f"{letter_column_classification}{row_num}"].fill = self.color_section(classification_color)
                    self.ws[f"{letter_column_sale}{row_num}"].fill = self.color_section(classification_color)




            #     print(obj)
            #
            #
            #     print(obj, kol)
            # else:
            #     print()



def preparing_data_loading_into(excel,slodnaya_bool):
    cla = PreDataLoadingInto
    data = cla(excel = excel,slodnaya_bool = slodnaya_bool).pars_data_loading_into()
    output = BytesIO()
    data.save(output)
    output.seek(0)

    return output