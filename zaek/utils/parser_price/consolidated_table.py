import os

import pandas as pd
from io import BytesIO

from base_app.utils.errors_plase import create_error


def float_func(kol):
    try:
        if pd.isna(kol):
            return 0.0
        return float(kol)
    except (ValueError, TypeError):
        return 0.0



def find_consolidated_table(file=None):
    try:
        df = pd.read_excel(file)
        new_data = {}
        for i , row in df.iterrows():
            art = row['Арт']
            kol = float_func(row['Кол'])

            if art:
                if new_data.get(art):
                    new_data[art] += kol
                else:
                    new_data[art] = kol
        print('ww')
        new_df = pd.DataFrame(list(new_data.items()),columns=['Арт','Кол'])

        b = BytesIO()
        with pd.ExcelWriter(b, engine='openpyxl') as writer:
            new_df.to_excel(writer, index=False, sheet_name='Запрос')
        b.seek(0)
        return b

    except Exception as e:
        create_error(
            name='parser_price_dist',
            path=os.path.abspath(__file__),
            error=e
        )




