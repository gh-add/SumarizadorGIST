from django import forms
from .models import Secao

class SecaoForm(forms.ModelForm):
    class Meta:
        model = Secao
        fields = ['tipo_entrada', 'url', 'arquivo']
        widgets = {
            'tipo_entrada': forms.Select(attrs={
                'class': 'form-select form-select-lg mb-3',
                'style': 'max-width: 500px;'
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': 'Digite a URL...',
                'style': 'max-width: 500px;'
            }),
            'arquivo': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg mb-3',
                'style': 'max-width: 500px;'
            }),
        }
