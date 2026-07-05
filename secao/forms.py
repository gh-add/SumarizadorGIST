from django import forms
from .models import Secao

class SecaoForm(forms.ModelForm):
    class Meta:
        model = Secao
        fields = ['tipo_entrada', 'url', 'arquivo']
        
