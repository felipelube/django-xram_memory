from django.db import models

from ..taxonomy.models import Keyword
from ..users.models import User
from ..base_models import TraceableModel
# Create your models here.


class ArchivedNews(TraceableModel):
    """
    Guarda uma notícia arquivada, enviada tanto manualmente ou obtida automaticamente pelo sistema do
    site.
    """

    STATUS_NEW = 100
    # Em fila
    STATUS_QUEUED_BASIC_INFO = 200
    STATUS_QUEUED_PAGE_CAPTURE = 201
    # Processado
    STATUS_PROCESSED_BASIC_INFO = 300
    STATUS_PROCESSED_PAGE_CAPTURE = 301
    STATUS_PROCESSED_ARCHIVED_NEWS_FETCHED = 302
    # Publicado
    STATUS_PUBLISHED = 400
    STATUS_PUBLISHED_HIDDEN = 401
    # Erros
    STATUS_ERROR_NO_PROCESS = 500
    STATUS_ERROR_NO_CAPTURE = 501
    STATUS_ERROR_NO_QUEUE = 502

    STATUS_CHOICES = (
        (STATUS_NEW, 'Novo'),

        (STATUS_QUEUED_BASIC_INFO, 'Em fila para buscar informações básicas'),
        (STATUS_QUEUED_PAGE_CAPTURE, 'Em fila para capturar a página'),


        (STATUS_PROCESSED_BASIC_INFO, 'Processado com informações básicas'),
        (STATUS_PROCESSED_PAGE_CAPTURE, 'Processado com captura de página'),
        (STATUS_PROCESSED_ARCHIVED_NEWS_FETCHED,
         'Processado com informações da página arquivada no Internet Archive'),

        (STATUS_PUBLISHED, 'Publicado'),
        (STATUS_PUBLISHED_HIDDEN, 'Publicado, mas escondido'),

        (STATUS_ERROR_NO_PROCESS, 'Erro no processamento básico'),
        (STATUS_ERROR_NO_CAPTURE, 'Erro na captura de página'),
        (STATUS_ERROR_NO_QUEUE, 'Erro no processamento automático'),
    )

    url = models.URLField(
        max_length=255, help_text="Endereço original da notícia",
        verbose_name="Endereço", unique=True, null=True, blank=True)

    archived_news_url = models.URLField(
        max_length=255, help_text="Endereço da notícia no <a href='https://archive.org/'>Archive.org</a>",
        verbose_name="Endereço no Internet Archive", unique=True, null=True, blank=True)

    title = models.CharField(max_length=255, blank=True,
                             help_text="Título da notícia", verbose_name="Título")

    status = models.PositiveIntegerField(
        default=STATUS_NEW, verbose_name="Status", editable=False, choices=STATUS_CHOICES)

    authors = models.TextField(
        blank=True, verbose_name="Autores", help_text='Nomes dos autores, separados por vírgula')

    images = models.TextField(
        blank=True, editable=False, verbose_name="Imagens", help_text="Imagens associadas a esta notícia")

    text = models.TextField(
        blank=True, verbose_name="Texto da notícia", help_text="Texto integral da notícia")

    top_image = models.ImageField(
        blank=True, verbose_name="Imagem principal")

    summary = models.TextField(
        blank=True, verbose_name="Resumo da notícia")

    keywords = models.ManyToManyField(
        Keyword, blank=True, verbose_name="Palavras-chave")

    published_date = models.DateTimeField(verbose_name='Data de publicação', blank=True, null=True,
                                          help_text='Data em que a notícia foi publicada')

    # Flags
    force_basic_processing = models.BooleanField(
        "Buscar automaticamente informações sobre a notícia", default=True,
        help_text="Marque se deseja incluir essa notícia para processamento automático.")
    force_archive_org_processing = models.BooleanField(
        "Buscar informações no Archive.org", default=True,
        help_text="Marque se deseja buscar uma versão arquivada desta notícia no <a href='https://archive.org/'>Archive.org</a>.")
    force_pdf_capture = models.BooleanField(
        "Capturar a notícia em formato PDF", default=True,
        help_text="Marque se deseja capturar essa notícia em formato PDF.")

    class Meta:
        verbose_name = "Archived News"
        verbose_name_plural = "Archived News"

    def __str__(self):
        return self.title

    @property
    def has_error(self):
        return str(self.status)[0] == '5'

    @property
    def needs_reprocessing(self):
        return self.force_basic_processing or self.force_archive_org_processing or self.force_pdf_capture

    @property
    def has_basic_info(self):
        # Não verifique o campo keywords se o modelo não estiver sido salvo para evitar uma exceção ValueError
        if self.pk is None:
            return (bool(self.text) or bool(self.summary) or bool(self.authors) or
                    bool(self.top_image) or bool(self.images) or bool(self.published_date))
        else:
            return (bool(self.text) or bool(self.summary) or bool(self.authors) or bool(self.keywords) or
                    bool(self.top_image) or bool(self.images) or bool(self.published_date))

    @property
    def has_pdf_capture(self):
        if self.pk is None:
            return False
        else:
            return bool(self.pdf_captures.count() > 0)

    @property
    def has_web_archive_url(self):
        return bool(self.archived_news_url)

    @property
    def is_published(self):
        return str(self.status)[0] == '4'

    @property
    def is_processed(self):
        return str(self.status)[0] == '3'

    @property
    def is_queued(self):
        return str(self.status)[0] == '2'

    @property
    def is_new(self):
        return self.status == ArchivedNews.STATUS_NEW
