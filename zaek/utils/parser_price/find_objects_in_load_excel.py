from django.db.models import Prefetch

from zaek.consts_zaek import split_parent_base, split_parent_obj
from zaek.models import Product, ClientClassificationDiscount, VolumeAtDiscount


class FindProductsInExcel:
    def __init__(self,request_products=None):
        self.request_products = request_products
        self.products = {}
        self.price_group_list_columns_to_sort=[]
        self.classification_columns_to_sort = []
        self.product = {}


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







    def create_dict(self):
        """Формируем объект в виде словаря"""
        for request_product in self.request_products:
            self.product['Артикул'] = request_product.art
            self.product['Цена (без НДС) руб.'] = request_product.price_not_nds
            self.product['Цена (с НДС) руб.'] = request_product.price_with_nds


            if request_product.classification:
                self.product['Классификация ПП'] = request_product.classification.name

                for discount in request_product.classification.classification_discounts.all():
                    discount_type_client_type = discount.type_client.type
                    self.product[discount_type_client_type] = discount.discount


                    if discount_type_client_type not in self.classification_columns_to_sort:
                        self.classification_columns_to_sort.append(discount_type_client_type)

            if request_product.price_group_list:
                self.get_price_group_list(request_product.price_group_list)



            print(self.product)





def find_objects_in_load_excel():
    artikul_list = ['344592', 'B002', '285971']


    # products = Product.objects.prefetch_related(
    #     'classification',
    #         Prefetch(
    #             'classification__classification_discounts',  # Скидки, связанные через ClassificationPriceProduct
    #             queryset=ClientClassificationDiscount.objects.select_related(
    #                 'type_client',
    #                 'classification_price_product',
    #             ).prefetch_related(
    #                 Prefetch(
    #                     'type_client__volume_discounts',
    #                     queryset=VolumeAtDiscount.objects.select_related(
    #                         'volume_level',
    #                         'classification_price_product'
    #                     ).order_by('volume_level__start_value')
    #                 ),
    #             ),
    #         ),
    #
    #     Prefetch(
    #         'classification__classification_volume_discounts',  # Скидки за объем, связанные через ClassificationPriceProduct
    #         queryset=VolumeAtDiscount.objects.select_related('volume_level', 'type_client'),
    #
    #     )


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

    ).filter(art__in=artikul_list)




    # for product in products:
    #     print(
    #         f"Продукт: {product}'\n"
    #         f"Артикул: {product.art}'\n"
    #     )
    #     if product.classification:
    #         print(f"Классификация: {product} = {product.classification}")
    #         for discount in product.classification.classification_discounts.all():
    #             print(f" - Скидка для {discount.type_client}: {discount.discount}%")
    #             #
    #             # for volume_discount in  discount.type_client.volume_discounts.all():
    #             #     print(volume_discount)
    #


    if products:
        new_excel_file = FindProductsInExcel
        new_excel_file(
            request_products=products
        ).create_dict()

