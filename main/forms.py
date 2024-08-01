from django import forms
from django.core.exceptions import ValidationError


class FileUploadMagaForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data['file']
        return file