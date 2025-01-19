from zaek.models import Product

list_object = [
'249256',
'341881',
'260503',
'260505',
'260506',
'260508'
]

def preparing_data_loading_into():
    products_filter  = Product.objects.filter(art__in = list_object)
    dict_products_filter = {obj.art:obj for obj in products_filter}
    products_filter = None

    


    print(dict_products_filter)