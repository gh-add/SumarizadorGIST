import os
from urllib.parse import urlparse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Secao
from algoritmo.services import GistSummService
import logging
logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Secao)
def pre_save_secao(sender, instance, **kwargs):
    url = instance.url
    arquivo = instance.arquivo
    if url:
        parsed_url = urlparse(url)
        path = parsed_url.path.strip("/")
        instance.nome = path.replace("/", " ") or parsed_url.netloc
    elif arquivo:
        filename = os.path.splitext(os.path.basename(arquivo.name))[0]
        instance.nome = filename.replace("_", " ")
    else:
        instance.nome = "secao_sem_fonte"

        
@receiver(post_save, sender=Secao)
def post_save_secao(sender, instance, created, **kwargs):
    if not created:
        return
    arquivo_path = instance.arquivo.path if instance.arquivo else None
    service = GistSummService()

    try:
        resumo, nome_imagem = service(
            tipo_entrada=instance.tipo_entrada,
            url=instance.url,
            arquivo=arquivo_path,
        )

    except Exception as e:
        print("Erro:", repr(e))
        raise

    instance.resumo = resumo
    instance.imagem_nuvem = nome_imagem
    instance.save(update_fields=["resumo", "imagem_nuvem"])