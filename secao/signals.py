import os
from urllib.parse import urlparse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Secao
from algoritmo.sumarizacao import get_dados

@receiver(pre_save, sender=Secao)
def pre_save_secao(sender, instance, **kwargs):
    url = instance.url
    arquivo = instance.arquivo

    if url:
        parsed_url = urlparse(url)
        path = parsed_url.path.strip("/")
        instance.nome = path.replace("/", "_") or parsed_url.netloc
    elif arquivo:
        filename = os.path.splitext(os.path.basename(arquivo.name))[0]
        instance.nome = filename.replace(" ", "_")
    else:
        instance.nome = "secao_sem_fonte"

@receiver(post_save, sender=Secao)
def post_save_secao(sender, instance, created, **kwargs):
    if created and not instance.texto_resposta:
        print("Arquivo salvo, processando resumo")
        url = instance.url
        arquivo = instance.arquivo
        arquivo_path = arquivo.path if arquivo else None

        resumo, nome_imagem = get_dados(instance.tipo_entrada, url, arquivo_path)

        instance.texto_resposta = resumo
        instance.imagem_nuvem = nome_imagem 
        instance.save(update_fields=['texto_resposta', 'imagem_nuvem'])

        
