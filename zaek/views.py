from django.shortcuts import render
from zaek.tasks import parse_price_zeak_file_task
from zaek.forms import FileUploadZeakForm
from zaek.utils.parser_price.need_price import CreatePriceExcel
from zaek.utils.parser_price.parser_price import test_start_price, ParserPrice


# Create your views here.
def index(request):
    return render(request, 'zaek/index.html')

def need_price(request):
    cl = CreatePriceExcel()
    cl.get_product_all()

    return render(request, template_name='zaek/need_price.html', )


def get_price(request):
    print('start')
    test_start_price()
    print('GOOD')
    return render(request, template_name='zaek/index.html',)
