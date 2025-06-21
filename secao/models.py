from django.db import models

class Secao(models.Model):
    TIPO_ENTRADA_CHOICES = [
        ('url', 'URL'),
        ('file', 'Arquivo'),
    ]

    nome = models.CharField(max_length=100)
    texto_resposta = models.TextField(blank=True)
    tipo_entrada = models.CharField(max_length=10, choices=TIPO_ENTRADA_CHOICES)
    url = models.URLField(blank=True, null=True) 
    arquivo = models.FileField(upload_to='uploads/', blank=True, null=True)  
    imagem_nuvem = models.CharField(max_length=255, blank=True, null=True)

