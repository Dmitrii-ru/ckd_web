import zipfile
import xml.etree.ElementTree as ET
import openpyxl
from django.db import transaction
from decimal import Decimal
from zaek.models import Product
from zaek.consts_zaek import base_columns, attrs_update_products, other_consts, split_parent_base, \
    split_parent_obj
from zaek.utils.parser_price.parser_price_dist import parser_price_dist

class ParserPrice:
    def __init__(
            self,
            price_path = None

    ):
        self.price_path = price_path
        self.header = None


    def load_shared_strings(self,zip_ref):
        shared_strings = []
        with zip_ref.open('xl/sharedStrings.xml') as shared_file:
            shared_tree = ET.parse(shared_file)
            shared_root = shared_tree.getroot()
            for si in shared_root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
                text = ''.join(node.text or '' for node in
                               si.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t'))
                shared_strings.append(text)
        print('load_shared_strings')
        return shared_strings


    def open_file(self):
        d = []

        with zipfile.ZipFile(self.price_path, 'r') as zip_ref:
            shared_strings = self.load_shared_strings(zip_ref)
            with zip_ref.open('xl/worksheets/sheet1.xml') as sheet_file:
                sheet_tree = ET.parse(sheet_file)
                sheet_root = sheet_tree.getroot()
                schema_rows = sheet_root.findall(
                    './/{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'
                )

                for schema_row in schema_rows:
                    outline_level = int(schema_row.get('outlineLevel', 0))
                    row_number = int(schema_row.get('r'))

                    row_data = []
                    for cell in schema_row.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
                        cell_type = cell.get('t')  # Проверка типа ячейки
                        cell_value = cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')

                        if cell_value is not None:
                            if cell_type == 's':  # Ячейка со строковым значением
                                value = shared_strings[int(cell_value.text)]
                            else:
                                value = cell_value.text
                            row_data.append(value)
                        else:
                            row_data.append(None)



                    if set(base_columns).issubset(row_data):
                        self.header = row_data
                        continue

                    if self.header:
                        row_data = dict(zip(self.header, row_data))
                        row_data['outline_level']=outline_level
                        d.append(row_data)
        print('open_file')
        return d





class PriceObject:

    def __init__(self,data_row):
        self.data_row = data_row
        self.level = 0
        self.art = None
        self.price_group = None
        self.name = 'Нет данных'
        self.unit = 0
        self.price_not_nds = 0
        self.price_with_nds = 0
        self.recommended_wholesale_price_not_nds = 0
        self.recommended_wholesale_price_with_nds = 0
        self.recommended_retail_price_not_nds = 0
        self.recommended_retail_price_with_nds =0
        self.stock_status_kursk = 0
        self.volume = 0
        self.weight = 0
        self.product_portfolio = 0
        self.packaging_norm = 0
        self.nomenclature_group = 'Нет данных'




    def parsing_object(self):
        for attr_name in vars(self):
            method_name = f'set_{attr_name}'
            if hasattr(self, method_name):
                method = getattr(self, method_name)
                method()

    @classmethod
    def convert_to_decimal(self,value):
        try:
            return Decimal(value)
        except Exception as e:
            return 0

    def set_level(self):
        self.level = self.data_row.get('outline_level',0)

    def set_art(self):
        self.art = self.data_row.get('Артикул', 'Не указан').replace(' ', '')

    def set_name(self):
        self.name = self.data_row.get('Номенклатура', 'Нет данных')

    def set_unit(self):
        self.unit = self.data_row.get('Ед.', 'Шт')

    def set_price_not_nds(self):
        value = self.data_row.get('Цена (без НДС) руб.', 0)
        self.price_not_nds = self.convert_to_decimal(value)

    def set_price_with_nds(self):
        value = self.data_row.get('Цена (с НДС) руб.', 0)
        self.price_with_nds = self.convert_to_decimal(value)

    def set_recommended_wholesale_price_not_nds(self):
        value = self.data_row.get('Рекоменд. оптовая цена (без НДС) руб.', 0)
        self.recommended_wholesale_price_not_nds = self.convert_to_decimal(value)

    def set_recommended_wholesale_price_with_nds(self):
        value = self.data_row.get('Рекоменд. оптовая цена (с НДС) руб.', 0)
        self.recommended_wholesale_price_with_nds = self.convert_to_decimal(value)

    def set_recommended_retail_price_not_nds(self):
        value = self.data_row.get('Рекоменд. розничная цена (без НДС) руб.', 0)
        self.recommended_retail_price_not_nds = self.convert_to_decimal(value)

    def set_recommended_retail_price_with_nds(self):
        value = self.data_row.get('Рекоменд. розничная цена (с НДС) руб.', 0)
        self.recommended_retail_price_with_nds = self.convert_to_decimal(value)

    def set_stock_status_kursk(self):
        self.stock_status_kursk = self.data_row.get('Складской статус в Курске', 0)

    def set_volume(self):
        value = self.data_row.get('Объем куб.м', 0)
        self.volume = self.convert_to_decimal(value)


    def set_weight(self):
        self.weight = self.data_row.get('Вес (кг)', 0)

    def set_product_portfolio(self):
        self.product_portfolio = self.data_row.get('Продуктовый портфель', 0)

    def set_packaging_norm(self):
        self.packaging_norm = self.data_row.get('Норма упаковки', 0)

    def set_nomenclature_group(self):
        self.nomenclature_group = self.data_row.get('Номенклатурная группа', 'Нет данных')

    def get_attrs_object(self):
        pass




class DataPrice(ParserPrice):
    def __init__(
            self,
            price_path=None
    ):

        super().__init__(price_path)
        self.parent_obj = None
        self.parent_tree = {}
        self.products_data = []

    def clean_parent_dict(self, outline_level, name_lvl):
        '''
        Убираю уровни ниже текущего
        '''

        self.parent_tree = {key: value for key, value in self.parent_tree.items() if key <= outline_level}
        self.parent_tree[outline_level] = name_lvl

    def get_parent_tree_string(self):
        sorted_tree = sorted(self.parent_tree.items())
        hierarchy = [f"{level}{split_parent_obj}{parent}" for level, parent in sorted_tree]
        parent_tree_str = f"{split_parent_base}".join(hierarchy)
        return parent_tree_str


    def get_price(self):
        price = self.open_file()
        unique_art = []

        for data_row in price:
            level = data_row.get('outline_level', 0)
            if not data_row['Артикул']:
                self.clean_parent_dict(level,data_row['Группа'])

            else:
                object_price = PriceObject(data_row)
                object_price.parsing_object()
                object_price.data_row = None
                object_price.price_group_list = self.get_parent_tree_string()

                if self.parent_obj:
                    object_price.price_group = None

                if object_price.art not in unique_art:
                    unique_art.append(object_price.art)
                    self.products_data.append(object_price)



        print('get_price')
        self.bulk_update_or_create_products()

    def bulk_update_or_create_products(self):
        existing_products = Product.objects.filter(art__in=[p.art for p in self.products_data])
        existing_products_dict = {product.art: product for product in existing_products}
        products_to_create = []
        products_to_update = []
        price_dist = parser_price_dist()
        price_group_2 = None
        summary_price_group = None
        classification = None
        str_not_data = other_consts.get('not_data','Нет данных')

        for data in self.products_data:
            price_dist_get_art = price_dist.get(str(data.art),None)

            if price_dist_get_art:
                price_group_2 = price_dist_get_art.get('Ценовая группа',str_not_data)
                summary_price_group = price_dist_get_art.get('Ценовая группа сводная',str_not_data)
                classification = price_dist_get_art.get('Классификация ПП',str_not_data)

            if data.art in existing_products_dict:
                product = existing_products_dict[data.art]
                product.price_group = data.price_group
                product.price_group_2 = price_group_2
                product.summary_price_group = summary_price_group
                product.classification = classification
                product.price_group_list = data.price_group_list
                product.price_not_nds = data.price_not_nds
                product.price_with_nds = data.price_with_nds

                products_to_update.append(product)

            else:
                products_to_create.append(Product(
                    level=data.level,
                    art=data.art,
                    name=data.name,
                    unit=data.unit,
                    price_not_nds=data.price_not_nds,
                    price_with_nds=data.price_with_nds,
                    recommended_wholesale_price_not_nds=data.recommended_wholesale_price_not_nds,
                    recommended_wholesale_price_with_nds=data.recommended_wholesale_price_with_nds,
                    recommended_retail_price_not_nds=data.recommended_retail_price_not_nds,
                    recommended_retail_price_with_nds=data.recommended_retail_price_with_nds,
                    stock_status_kursk=data.stock_status_kursk,
                    volume=data.volume,
                    weight=data.weight,
                    product_portfolio=data.product_portfolio,
                    packaging_norm=data.packaging_norm,
                    nomenclature_group=data.nomenclature_group,
                    price_group_2=price_group_2,
                    summary_price_group=summary_price_group,
                    classification=classification,
                    price_group_list=data.price_group_list

                )
                )


        with transaction.atomic():
            batch_size =1000
            if products_to_create:
                Product.objects.bulk_create(products_to_create,batch_size=batch_size)

            if products_to_update:
                for i in range(0, len(products_to_update), batch_size):
                    batch = products_to_update[i:i + batch_size]
                    Product.objects.bulk_update(batch, attrs_update_products)


    def delete_file(self,file_instance):
        from django.core.files.storage import default_storage
        try:
            file_path = file_instance.file.name

            if default_storage.exists(file_path):
                default_storage.delete(file_path)

            file_instance.delete()
        except Exception as e:
            print(f'Error deleting file: {e}')

