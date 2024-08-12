import pandas as pd
from django.shortcuts import render
from core_app.redis_cli import RedisClientMain
from main.forms import FileUploadMagaForm, FileUploadFindProductsCode
from main.unils.parser_magadel.parser_maga_file import parser_maga_file_func
from .models import *
from .unils.find_products_code.find_products_code import find_products_code_func
from .unils.parser_magadel.const import sheet_name, const
from django.http import HttpResponse
from io import BytesIO


def index(request):
    return render(request, 'main/index.html')


def upload_maga(request):
    form = FileUploadMagaForm()
    if request.method == 'POST':
        form = FileUploadMagaForm(request.POST, request.FILES)
        if form.is_valid():
            result_error = parser_maga_file_func(request.FILES['file'])

            if result_error:
                return render(request, 'main/info.html', context={'massage': result_error})
            else:
                return render(request, 'main/info.html', context={'massage': 'Файл успешно загружен'})

    return render(
        request, 'main/upload_maga.html',
        {'form': form, "sheet_name": sheet_name, 'columns_list': ", ".join(list(const.values()))}
    )


def find_products_code(request):
    form = FileUploadFindProductsCode()
    if request.method == 'POST':
        form = FileUploadFindProductsCode(request.POST, request.FILES)
        if form.is_valid():
            output, name = find_products_code_func(request.FILES['file'])

            output.seek(0)
            response = HttpResponse(
                output,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="{name}"; filename*=UTF-8\'\'{name}'

            return response

    return render(request, 'main/find_products_code.html', {'form': form})
