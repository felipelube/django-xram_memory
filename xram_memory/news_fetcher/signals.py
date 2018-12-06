from django.dispatch import receiver
from django.db.models.signals import post_save
from ..archived_news.models import ArchivedNews
from .fetcher import process_news, save_news_as_pdf
import logging
import django_rq


logger = logging.getLogger(__name__)


@receiver(post_save, sender=ArchivedNews)
def add_news_archive_to_queue(sender, **kwargs):
    try:
        archived_news = kwargs['instance']
        if not archived_news:
            return
        if hasattr(archived_news, '_dirty'):
            return

        if (archived_news.status == ArchivedNews.STATUS_NEW or
                archived_news.status == ArchivedNews.STATUS_ERROR):
            logger.info(
                'Notícia com o id {} e status "{}" inserida na fila para processamento.'.format(
                    archived_news.id, archived_news.get_status_display()
                )
            )
            try:
                # @todo verificar se o serviço de filas está funcionando (se existe conexão com o redis)
                # e logar um aviso caso contrário
                # Adicione uma flag ao objeto para evitar que esse hadler execute infinitamente,
                # já que algumas das funções abaixo podem chamar o save()
                archived_news._dirty = True

                process_news.delay(archived_news)
                save_news_as_pdf.delay(archived_news)
                # adicione a notícia na fila para  baixar
                # altere o status para 'agendado'
                # salve o modelo
            finally:
                del archived_news._dirty
    except:
        pass
