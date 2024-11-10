from django.http import HttpResponse
from django.shortcuts import render

from zaek.utils.parser_price.need_price import need_price_func
from zaek.utils.parser_price.parser_price import test_start_price



def index(request):
    return render(request, 'zaek/index.html')





def get_price(request):

    print('start')
    test_start_price()
    print('GOOD')
    return render(request, template_name='zaek/index.html',)


def need_price(request):

    try:
        from urllib.parse import quote
        price, name = need_price_func()
        file_path = price.file.path
        with open(file_path, 'rb') as f:
            file_content = f.read()
        new_name = quote(name)
        response = HttpResponse(
            file_content,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={new_name}.xlsx'  # Убедитесь, что имя файла с расширением .xlsx
        return response
    except Exception as e:
        return render(request, 'zaek/info.html', context={'massage': f'Сервер в отпуске ({e})'})
