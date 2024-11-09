from django.shortcuts import render
import requests

# Create your views here.
def start_page(request):
    return render(request, 'base_app/start_page.html')


def get_currency(request):
    API_URL = 'https://www.cbr-xml-daily.ru/latest.js'  # пример API
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        print(data)
    return render(request, 'base_app/start_page.html')