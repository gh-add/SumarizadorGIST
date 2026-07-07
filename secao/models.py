from django.db import models

class Secao(models.Model):
    TIPO_ENTRADA_CHOICES = [
        ('url', 'URL'),
        ('file', 'Arquivo'),
    ]
    STATUS_CHOICES = [
        ('processando', 'Processando'),
        ('concluido', 'Concluído'),
        ('erro', 'Erro'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processando')
    nome = models.CharField(max_length=100)
    resumo = models.TextField(blank=True, null=True)
    tipo_entrada = models.CharField(max_length=10, choices=TIPO_ENTRADA_CHOICES)
    url = models.URLField(blank=True, null=True) 
    arquivo = models.FileField(upload_to='uploads/', blank=True, null=True)  
    imagem_nuvem = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

