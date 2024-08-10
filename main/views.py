from django.shortcuts import render

from main.forms import FileUploadMagaForm
from main.unils.parser_magadel.parser_maga_file import parser_maga_file_func


def index(request):
    return render(request, 'main/index.html')


def upload_maga(request):
    form = FileUploadMagaForm()
    if request.method == 'POST':
        form = FileUploadMagaForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                parser_maga_file_func(request.FILES['file'])
                print(f"Все гуд --- def upload_maga(request):")
            except:
                print('Ошибка --- def upload_maga(request):')

    return render(request, 'main/upload_maga.html', {'form': form})
