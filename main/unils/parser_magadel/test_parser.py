import pandas as pd


def check_float(x):
    try:
        return float(x)
    except:
        return 0


def get_columns_possible_deliveries(columns_possible_deliveries,columns):
    '''
    Получаем колонки с датами
    '''

    for column in columns:


            pd.to_datetime(column)


            columns_possible_deliveries.append(pd.to_datetime(column))




def possible_deliveries_fanc(columns_possible_deliveries, row):
    '''
    Получаем общий список дат, где есть значение
    '''

    summ = 0
    list_possible_deliveries_date = ''
    for i in columns_possible_deliveries:
        try:
            value = row.get(i, None)
            if value:
                summ += check_float(value)
                if list_possible_deliveries_date:
                    list_possible_deliveries_date += f', {i} - {value}'
                else:
                    list_possible_deliveries_date = f'{i} - {value}'

        except:
            return '', 0
    return list_possible_deliveries_date, summ


row = {
    '22.22.22': 0,
    'wqw': 3
}
columns_possible_deliveries = []
get_columns_possible_deliveries(columns_possible_deliveries,{'22.22.1122': 2, 'wqw': 3})
possible_deliveries, possible_deliveries_sum = possible_deliveries_fanc(
    columns_possible_deliveries, row
)

print(columns_possible_deliveries)
