from django.apps import apps
from django.db import transaction
from celery import shared_task, group
from django.db.utils import IntegrityError, OperationalError
from django.core.exceptions import ValidationError


PROCESSING_TASK_TIMEOUT = 300
FETCH_TASK_TIMEOUT = 30


@shared_task(
    autoretry_for=(OperationalError, ConnectionError),
    retry_backoff=5,
    max_retries=10,
    retry_backoff_max=300,
    retry_jitter=True,
    throws=(ValidationError,),
    time_limit=PROCESSING_TASK_TIMEOUT,
    rate_limit="10/m",
)
def newspaper_set_basic_info(newspaper_id):
    """
    Define informações básicas sobre um Jornal
    """
    Newspaper = apps.get_model("artifact", "Newspaper")
    newspaper = Newspaper.objects.get(pk=newspaper_id)
    newspaper._save_in_signal = True
    try:
        newspaper.set_basic_info()
        newspaper.save()
    except:
        raise
    else:
        return newspaper
    finally:
        del newspaper._save_in_signal


@shared_task(
    autoretry_for=(OperationalError, ConnectionError),
    retry_backoff=5,
    max_retries=10,
    retry_backoff_max=300,
    retry_jitter=True,
    throws=(ValueError,),
    time_limit=PROCESSING_TASK_TIMEOUT,
    rate_limit="10/m",
)
def newspaper_set_logo_from_favicon(newspaper_id):
    """
    Adiciona um logotipo para o Jornal com base no seu favicon
    """
    Newspaper = apps.get_model("artifact", "Newspaper")
    newspaper = Newspaper.objects.get(pk=newspaper_id)
    newspaper._save_in_signal = True
    try:
        newspaper.set_logo_from_favicon()
        newspaper.save()
    except:
        raise
    finally:
        del newspaper._save_in_signal


@shared_task(
    autoretry_for=(OperationalError, ConnectionError),
    retry_backoff=5,
    max_retries=10,
    retry_backoff_max=300,
    retry_jitter=True,
    throws=(
        ValidationError,
        ValueError,
    ),
    time_limit=PROCESSING_TASK_TIMEOUT,
    rate_limit="10/m",
)
def news_set_basic_info(news_id, sync=False):
    """
    Define informações básica sobre uma Notícia. Com base nessas informações,  agenda/executa a obtenção/inserção de uma
    imagem associada a ela e de palavras-chave.
    """
    News = apps.get_model("artifact", "News")
    news = News.objects.get(pk=news_id)
    try:
        news.set_basic_info()
        news.save()

        if getattr(news, "_image", None):
            if sync:
                add_image_for_news(news._image, news_id)
            else:
                add_image_for_news.delay(news._image, news_id)
        if getattr(news, "_keywords", None):
            if sync:
                add_keywords_for_news(news._keywords, news_id)
            else:
                add_keywords_for_news.delay(news._keywords, news_id)
        if getattr(news, "_subjects", None):
            if sync:
                add_subjects_for_news(news._subjects, news_id)
            else:
                add_subjects_for_news.delay(news._subjects, news_id)
    except:
        raise
    else:
        return news


@shared_task(
    autoretry_for=(OperationalError,),
    retry_backoff=5,
    max_retries=10,
    retry_backoff_max=300,
    retry_jitter=True,
    rate_limit="10/m",
)
def add_keywords_for_news(keywords, news_id):
    """
    Cria uma instância de uma Palavra-chave (Taxonomia) para cada palavra-chave identificada por `news_set_basic_info`
    e associa ela à Notícia.
    """
    News = apps.get_model("artifact", "News")
    news = News.objects.get(pk=news_id)
    try:
        news._keywords = keywords
        news.add_fetched_keywords()
    except:
        raise
    else:
        return True


@shared_task(
    autoretry_for=(OperationalError,),
    retry_backoff=5,
    max_retries=10,
    retry_backoff_max=300,
    retry_jitter=True,
    rate_limit="10/m",
)
def add_subjects_for_news(subjects, news_id):
    """
    Cria uma instância de um Assunto (Taxonomia) para cada assunto identificado por
    `news_set_basic_info` e associa ele à Notícia.
    """
    News = apps.get_model("artifact", "News")
    news = News.objects.get(pk=news_id)
    try:
        news._subjects = subjects
        news.add_fetched_subjects()
    except:
        raise
    else:
        return True


@shared_task(
    autoretry_for=(
        OperationalError,
        ConnectionError,
    ),
    retry_backoff=5,
    max_retries=10,
    retry_backoff_max=300,
    retry_jitter=True,
)
def add_image_for_news(image_url, news_id):
    """
    Com base na url de imagem identificada por `news_set_basic_info`, baixa, cria um documento de captura de imagem e
    associa ele à Notícia informada.
    """
    News = apps.get_model("artifact", "News")
    news = News.objects.get(pk=news_id)
    try:
        news._image = image_url
        news.add_fetched_image()
        return news.image_capture
    except:
        raise
    else:
        return True


@shared_task(
    autoretry_for=(OperationalError, ConnectionError),
    retry_backoff=5,
    max_retries=10,
    retry_backoff_max=300,
    retry_jitter=True,
    throws=(ValidationError,),
    time_limit=PROCESSING_TASK_TIMEOUT,
    rate_limit="10/m",
)
def news_add_archived_url(news_id):
    """
    Busca e adiciona a URL para uma versão arquivada da notícia no Archive.org.
    """
    News = apps.get_model("artifact", "News")
    news = News.objects.get(pk=news_id)
    try:
        news.fetch_archived_url()
        news.save()
    except:
        raise
    else:
        if news.archived_news_url:
            return news.archived_news_url
        else:
            return True


@shared_task(
    throws=(OSError,),
    autoretry_for=(
        OperationalError,
        ConnectionError,
    ),
    retry_backoff=5,
    max_retries=10,
    retry_backoff_max=300,
    retry_jitter=True,
    time_limit=PROCESSING_TASK_TIMEOUT,
    rate_limit="10/m",
)
def news_add_pdf_capture(news_id):
    """
    Com base na url da notícia, baixa a página dela em formato PDF, cria um documento de captura e associa ele
    à Notícia informada.
    """
    News = apps.get_model("artifact", "News")
    news = News.objects.get(pk=news_id)
    try:
        news.add_pdf_capture()
    except:
        raise
    else:
        return True


# TODO: tratar exceção ValueError
# TODO: adicionar um registro de inserção na interface administrativa
@shared_task(
    autoretry_for=(OperationalError, ConnectionError),
    retry_backoff=5,
    max_retries=10,
    retry_backoff_max=300,
    retry_jitter=True,
    time_limit=PROCESSING_TASK_TIMEOUT,
)
def add_news_task(url, user_id):
    """
    Cria uma notícia com apenas o título e a URL. Agenda tarefas adicionais para pegar informações a mais sobre esta
    notícia.
    """
    News = apps.get_model("artifact", "News")
    User = apps.get_model("users", "User")
    try:
        user = User.objects.get(pk=user_id)
        # 1) Crie uma notícia com o usuário informado
        news = News(url=url, created_by=user, modified_by=user)
        # 2) Salve a notícia
        news.save()
        # 3) Agende trabalhos para obter informações adicionais
        transaction.on_commit(
            lambda news=news: group(
                [
                    news_set_basic_info.s(news.pk),
                    news_add_archived_url.s(news.pk),
                    news_add_pdf_capture.s(news.pk),
                ]
            ).apply_async()
        )
        return news.pk
    # TODO: verificar por que a exceção IntegrityError não está sendo ignorada pelo parâmetro throws na tarefa
    except IntegrityError:
        # não faça nada em caso duma notícia já existente
        pass
    except:
        raise
