

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

price_groups = 'Прайс с группами товаров'
delimiter_price_csv = ';'
zaek_sheet = 'TDSheet'
split_parent_base = '//*//'
split_parent_obj = '-'
custom_price_name = 'Кастомизированный прайс'
price_name = 'keaz'
classification_str = 'Классификация ПП'


price_groups_names_consts = {
    'ПП KEAZ Optima':'ПП KEAZ Optima',
    'ПП KEAZ':'ПП KEAZ',
    'ПП КЭАЗ исключение':f'ПП КЭАЗ исключение {", ".join(exception_values)}',
    'ПП KEAZ Optima Проектный':'ПП KEAZ Optima Проектный'
}



discount_distributor_price_groups = {
    "Платиновый": {
        price_groups_names_consts.get('ПП KEAZ Optima'): 60,
        price_groups_names_consts.get('ПП KEAZ'): 60,
        price_groups_names_consts.get('ПП КЭАЗ исключение ВА57, ВА57Ф, ВА51, ВА04'): 60,
        price_groups_names_consts.get('ПП KEAZ Optima Проектный'): 40
    },

    "Премиум": {
        price_groups_names_consts.get('ПП KEAZ Optima'): 57,
        price_groups_names_consts.get('ПП KEAZ'): 57,
        price_groups_names_consts.get('ПП КЭАЗ исключение ВА57, ВА57Ф, ВА51, ВА04'): 50,
        price_groups_names_consts.get('ПП KEAZ Optima Проектный'): 37
    }
}


discount_csho_price_groups = {
    "Прямой": {
        price_groups_names_consts.get('ПП KEAZ Optima'): 60,
        price_groups_names_consts.get('ПП KEAZ'): 55,
        price_groups_names_consts.get('ПП КЭАЗ исключение ВА57, ВА57Ф, ВА51, ВА04'): 55,
        price_groups_names_consts.get('ПП KEAZ Optima Проектный'): 60
    },

    "Золотой 3-х": {
        price_groups_names_consts.get('ПП KEAZ Optima'): 54,
        price_groups_names_consts.get('ПП KEAZ'): 54,
        price_groups_names_consts.get('ПП КЭАЗ исключение ВА57, ВА57Ф, ВА51, ВА04'): 54,
        price_groups_names_consts.get('ПП KEAZ Optima Проектный'): 54
    },

    "Серебряный 3-х": {
        price_groups_names_consts.get('ПП KEAZ Optima'): 53,
        price_groups_names_consts.get('ПП KEAZ'): 53,
        price_groups_names_consts.get('ПП КЭАЗ исключение ВА57, ВА57Ф, ВА51, ВА04'): 53,
        price_groups_names_consts.get('ПП KEAZ Optima Проектный'): 53
    }
}


discount_projects_groups = {
        price_groups_names_consts.get('ПП KEAZ Optima'): 'Optima',
        price_groups_names_consts.get('ПП KEAZ'): 'KEAZ',
        price_groups_names_consts.get('ПП КЭАЗ исключение ВА57, ВА57Ф, ВА51, ВА04'): 'KEAZ',
        price_groups_names_consts.get('ПП KEAZ Optima Проектный'): 'Optima'
}

discount_groups_price_consts = {
            "От 1.2": 1200000,
            "От 2": 2000000,
            "От 5": 5000000,
            "От 10": 10000000,
            "От 15": 15000000
}




discount_groups_price = {
    "Дист": {
        "Платиновый": {
            discount_groups_price_consts.get("От 1.2"): {"КАЕЗ": 60, "Optima": 60},
            discount_groups_price_consts.get("От 2"): {"КАЕЗ": 61, "Optima": 62},
            discount_groups_price_consts.get("От 5"): {"КАЕЗ": 62, "Optima": 64},
            discount_groups_price_consts.get("От 10"): {"КАЕЗ": 63, "Optima": 66},
            discount_groups_price_consts.get("От 15"): {"КАЕЗ": 64, "Optima": 68}
        },

    },
    "СЩО": {
        "Прямой": {
            discount_groups_price_consts.get("От 1.2"): {"КАЕЗ": 60, "Optima": 60},
            discount_groups_price_consts.get("От 2"): {"КАЕЗ": 61, "Optima": 62},
            discount_groups_price_consts.get("От 5"): {"КАЕЗ": 62, "Optima": 64},
            discount_groups_price_consts.get("От 10"): {"КАЕЗ": 63, "Optima": 66},
            discount_groups_price_consts.get("От 15"): {"КАЕЗ": 64, "Optima": 68}
        },
        "3-х": {
            discount_groups_price_consts.get("От 1.2"): {"КАЕЗ": 54, "Optima": 56},
            discount_groups_price_consts.get("От 2"): {"КАЕЗ": 57, "Optima": 58},
            discount_groups_price_consts.get("От 5"): {"КАЕЗ": 58, "Optima": 60},
            discount_groups_price_consts.get("От 10"): {"КАЕЗ": 59, "Optima": 62},
            discount_groups_price_consts.get("От 15"): {"КАЕЗ": 60, "Optima": 64}
        }
    }
}



