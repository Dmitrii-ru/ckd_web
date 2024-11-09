



from django.shortcuts import render



from stock.utils.rates import RatesCbr




def stock_data(request):
    rates = RatesCbr()

    cnt = {
        'rates':rates.get_rates()
    }

    return render(
        request,
        context=cnt,
        template_name='stock/index.html'
    )