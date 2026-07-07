import os
import threading
import logging
from urllib.parse import urlparse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Secao
from algoritmo.services import GistSummService

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


def _processar_resumo_thread(pk):
    service = GistSummService()
    try:
        secao = Secao.objects.get(pk=pk)
        resumo, nome_imagem = service(
            tipo_entrada=secao.tipo_entrada,
            url=secao.url,
            arquivo=secao.arquivo.path if secao.arquivo else None
        )
        secao.resumo = resumo
        secao.imagem_nuvem = nome_imagem
        secao.status = 'concluido'
        secao.save(update_fields=["resumo", "imagem_nuvem", "status"])
    except Exception as e:
        try:
            secao = Secao.objects.get(pk=pk)
            secao.status = 'erro'
            secao.save(update_fields=["status"])
            logger.exception(f"Erro ao processar resumo da seção {pk}: {e}")
        except Secao.DoesNotExist:
            logger.error(f"Seção com ID {pk} não encontrada para atualizar status de erro.")


@receiver(post_save, sender=Secao)
def post_save_secao(sender, instance, created, **kwargs):
    if not created:
        return
    thread = threading.Thread(target=_processar_resumo_thread, args=(instance.pk,))
    thread.daemon = True
    thread.start()