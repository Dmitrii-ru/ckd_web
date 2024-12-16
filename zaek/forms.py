from django.core.exceptions import ValidationError
from django import forms
from zaek.models import ZaekPrice


# def validate_columns_df(list_columns, df, sheet_name=None):
#     header = None
#     try:
#         list_columns_set = set(list_columns)
#         workbook = openpyxl.load_workbook(df, read_only=True, data_only=True)
#         if sheet_name:
#             if sheet_name not in workbook.sheetnames:
#                 raise ValidationError(f'Лист с именем "{sheet_name}" не найден в файле.')
#             workbook = workbook[sheet_name]
#
#         for i, row in enumerate(workbook.iter_rows(values_only=True)):
#             if list_columns_set.issubset(set(row)):
#
#                 header = i
#                 break
#
#         if header is None:
#             raise ValidationError(f'Нет нужных колонок {list_columns}')
#         return header
#
#     except Exception as e:
#         raise ValidationError(f'Ошибка при проверки файла {e}')





class PriceLoadZaekForm(forms.Form):

    file = forms.FileField(
        label='Файл',
        required=True
    )

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file:
            raise ValidationError('Вы ничего не загрузили')
        if not str(file).endswith('.xlsx'):
            raise ValidationError('Формат должен быть .xlsx')
        return file

class PriceLoadZaekGroupsForm(forms.Form):

    file = forms.FileField(
        label='Файл',
        required=True
    )

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file:
            raise ValidationError('Вы ничего не загрузили')
        if not str(file).endswith('.csv'):
            raise ValidationError('Формат должен быть .xlsx')
        return file

class ConsolidatedTableForm(forms.Form):

    file = forms.FileField(
        label='Файл',
        required=True
    )

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file:
            raise ValidationError('Вы ничего не загрузили')
        if not str(file).endswith('.xlsx'):
            raise ValidationError('Формат должен быть .xlsx')
        return file