from django.http import HttpResponse
from django.shortcuts import render
from .consts_zaek import base_columns, zaek_sheet, custom_price_name, price_name, price_groups, delimiter_price_csv
from .forms import PriceLoadZaekForm,PriceLoadZaekGroupsForm
from zaek.utils.parser_price.need_price import need_price_func
from .models import ZaekPrice
from django.utils import timezone
from .tasks import get_price_task


def index(request):
    return render(
        request,
        context={
            'custom_price_name': custom_price_name.lower(),
            'price_name': price_name.lower(),
        },
        template_name='zaek/index.html'
    )


def price_menu_load(request):
    return render(
        request,
        context={
            'price_groups': price_groups.lower(),
            'price_name': price_name.lower(),
        },
        template_name='zaek/price_menu_load.html'
    )




def get_price(request):
    if request.method == 'POST':
        form = PriceLoadZaekForm(request.POST, request.FILES)
        if form.is_valid():
            zaek_price, created = ZaekPrice.objects.get_or_create(
                name=price_name,
                defaults={'created_at': timezone.now()}
            )

            if not created and zaek_price.file:
                zaek_price.file.delete(save=False)
            zaek_price.file = form.cleaned_data['file']
            zaek_price.save()
            get_price_task.delay(zaek_price.file.path)
            return render(request, 'zaek/info.html',
                          context={'massage': 'Идет загрузка файла, можете покинуть страницу '})
    else:
        form = PriceLoadZaekForm()


    return render(
        request, 'zaek/upload_zaek.html',
        {
            'form': form,
            "sheet_name": zaek_sheet,
            'columns_list': ", ".join(base_columns)
        }
    )



def need_price(request):
    try:
        from urllib.parse import quote
        try:
            price, name = need_price_func()
            file_path = price.file.path
        except:
            return render(
                request,
                template_name='zaek/info.html',
                context={'massage': f'Данные не готовы, попробуйте через пару минут!'}
            )
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
        return render(
            request,
            template_name='zaek/info.html',
            context={'massage': f'Сервер в отпуске ({e})'}
        )



def get_price_groups(request):
    if request.method == 'POST':
        form = PriceLoadZaekGroupsForm(request.POST, request.FILES)
        if form.is_valid():

            zaek_price, created = ZaekPrice.objects.get_or_create(
                name=price_groups,
                defaults={'created_at': timezone.now()}
            )
            if not created and zaek_price.file:
                zaek_price.file.delete(save=False)
            zaek_price.file = form.cleaned_data['file']
            zaek_price.save()
            return render(request, 'zaek/info.html',
                          context={'massage': 'Идет загрузка файла, можете покинуть страницу '})
    else:
        form = PriceLoadZaekGroupsForm()

    return render(
        request, 'zaek/upload_zaek_groups.html',
        {
            'form': form,
            "delimiter_price_csv": delimiter_price_csv,
            'columns_list': ", ".join(base_columns)
        }
    )

