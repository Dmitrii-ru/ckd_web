

base_columns = [
    'Группа', 'Артикул',
    'Номенклатура', 'Ед.',
    'Цена (без НДС) руб.',
    'Цена (с НДС) руб.',
    'Рекоменд. оптовая цена (без НДС) руб.',
    'Рекоменд. оптовая цена (с НДС) руб.',
    'Рекоменд. розничная цена (без НДС) руб.',
    'Рекоменд. розничная цена (с НДС) руб.',
    'Складской статус в Курске',
    'Объем куб.м',
    'Вес (кг)',
    'Продуктовый портфель',
    'Норма упаковки',
    'Номенклатурная группа'
]



attrs_update_products = [
    'level', 'art',
    'name', 'unit', 'price_not_nds', 'price_with_nds',
    'recommended_wholesale_price_not_nds', 'recommended_wholesale_price_with_nds',
    'recommended_retail_price_not_nds', 'recommended_retail_price_with_nds',
    'stock_status_kursk', 'volume', 'weight',
    'product_portfolio', 'packaging_norm', 'nomenclature_group',
    'price_group_2','summary_price_group','classification','price_group_list'
]

other_consts= {
    'not_data' : 'Нет данных'
}

exception_values = ['ВА57','ВА57Ф','ВА51','ВА04']
extra_values =['Комплекты зажимов' , 'Аксессуары']

split_parent_base = '//*//'
split_parent_obj = '-'
custom_price_name = 'Кастомизированный прайс'