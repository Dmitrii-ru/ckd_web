from django.shortcuts import render

from main.forms import FileUploadMagaForm
from .unils.parser_maga_file import parser_maga_file_func


def index(request):
    return render(request, 'main/index.html')


def upload_maga(request):
    form = FileUploadMagaForm()
    if request.method == 'POST':
        form = FileUploadMagaForm(request.POST, request.FILES)
        if form.is_valid():
            maga_file = request.FILES['file']
            parser_maga_file_func(maga_file)
    return render(request, 'main/upload_maga.html', {'form': form})
