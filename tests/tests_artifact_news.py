import pytest
import hashlib
import factory
import datetime
from xram_memory.taxonomy.models import Keyword, Subject
from xram_memory.lib import NewsFetcher
from xram_memory.artifact.models import News, NewsImageCapture, NewsPDFCapture
from unittest.mock import patch
from loguru import logger
from django.test import TransactionTestCase
from django.db.models.signals import post_save, m2m_changed, pre_delete, post_delete
from .utils import basic_news_with_newspaper as basic_news
from . import fixtures
from .utils import DisabledIndexingAppsMixin

logger.remove()

# Create your tests here.

# TODO: Quando for buscar uma notícia na web, usar uma fixture, já que essa notícia pode ser retirada do ar
# TODO: converter para o estilo pytest quando https://github.com/pytest-dev/pytest-django/pull/721 for aceita


@pytest.mark.django_db(transaction=True)
class NewsTestCase(DisabledIndexingAppsMixin, TransactionTestCase):
    serialized_rollback = True

    def test_require_url_on_save(self):
        """
        Verifica se uma exceção ValueError é invocada numa tentativa de salvar
        uma Notícia sem URL.
        """
        news = News(title="Abacate")
        self.assertRaises(ValueError, news.save)

    @factory.django.mute_signals(post_save, m2m_changed, pre_delete, post_delete)
    def test_save_without_title(self):
        """
        Verifica se uma notícia é salva com um título mesmo no caso dos plugins
        de obtenção de informações não rodarem.
        """
        news = News(
            url="https://internacional.estadao.com.br/noticias/geral,venezuela-anuncia-reabertura-da-fronteira-com-brasil-e-aruba,70002823580"
        )
        news.save()
        self.assertNotEqual(news.title, "")

    def test_string_value(self):
        """
        Verifica a implentação de __str__ para notícia.
        """
        news = News(
            url="https://internacional.estadao.com.br/noticias/geral,venezuela-anuncia-reabertura-da-fronteira-com-brasil-e-aruba,70002823580"
        )
        self.assertEqual(str(news), "(sem título)")
        news.title = "Um teste"
        self.assertEqual(str(news), news.title)

    def test_initial_flags_state(self):
        """
        Verifica o estado inicial de várias flags e propriedades de Notícia
        """
        news = News(
            url="https://internacional.estadao.com.br/noticias/geral,venezuela-anuncia-reabertura-da-fronteira-com-brasil-e-aruba,70002823580"
        )
        for field in [
            "thumbnail",
            "published_year",
            "image_capture_indexing",
            "body",
            "teaser",
            "published_date",
        ]:
            value = getattr(news, field)
            self.assertIsNone(value)

        for field in [
            "title",
            "authors",
        ]:
            value = getattr(news, field)
            self.assertEqual(value, "")

        for field in [
            "has_basic_info",
            "has_pdf_capture",
            "has_image",
        ]:
            value = getattr(news, field)
            self.assertFalse(value)

    def test_set_web_title(self):
        """
        Verifica o funcionamento de news.set_web_title(), que deve popular
        news.title.
        """
        news = News(
            url="https://brasil.elpais.com/brasil/2015/12/29/economia/1451418696_403408.html"
        )
        self.assertEqual(news.title, "")
        with patch.object(NewsFetcher, "fetch_web_title") as mocked:
            mocked.return_value = "Dilma paga pedaladas até de 2015 para enfraquecer argumento do impeachment"
            news.set_web_title()
            self.assertNotEqual(news.title, "")

    def test_fetch_archived_url(self):
        """
        Verifica o funcionamento de news.fetch_archived_url(), que deve popular
        news.archived_news_url
        """
        news = News(
            url="https://brasil.elpais.com/brasil/2015/12/29/economia/1451418696_403408.html"
        )
        self.assertIsNone(news.archived_news_url)
        with patch.object(NewsFetcher, "fetch_archived_url") as mocked:
            mocked.return_value = fixtures.mocked_news_fetch_archived_url(news.url)
            news.fetch_archived_url()
            self.assertIsNotNone(news.archived_news_url)

    def test_set_basic_info(self):
        """
        Verifica o funcionamento de news.set_basic_info(), que deve popular
        várias propriedades de News.
        """
        news = News(
            url="https://brasil.elpais.com/brasil/2015/12/29/economia/1451418696_403408.html"
        )

        # Atributos que não podem estar em branco ('')
        not_blank_attrs = ["title", "authors"]
        # Atributos que não podem estar nulos (None)
        not_null_attrs = ["body", "teaser", "published_date", "language"]
        # Atributos especiais, que começam com '_' e que não podem estar nulos (None)
        under_attrs = ["image", "keywords", "subjects"]

        expected_response_keys = [*not_blank_attrs, *not_null_attrs, *under_attrs]

        with patch.object(
            NewsFetcher, "fetch_basic_info", return_value=fixtures.NEWS_INFO_MOCK
        ):
            result = news.set_basic_info()

            for expected_key in expected_response_keys:
                self.assertIn(expected_key, result.keys())

            for not_blank_attr in not_blank_attrs:
                value = getattr(news, not_blank_attr)
                self.assertNotEqual(value, "")

            for not_null_attr in not_null_attrs:
                value = getattr(news, not_null_attr)
                self.assertIsNotNone(value)
                if not_null_attr == "published_date":
                    # 'published_date' deve ser do tipo data/tempo...
                    self.assertIsInstance(value, datetime.datetime)
                    # ...e deve conter informações do fuso-horário (não pode ser uma data ingênua)
                    self.assertIsNotNone(news.published_date.tzinfo)

            for under_attr in under_attrs:
                value = getattr(news, "_{}".format(under_attr))
                self.assertIsNotNone(value)
                if under_attr in ("_keywords", "_subjects"):
                    self.assertIsInstance(value, list)

    @factory.django.mute_signals(post_save, m2m_changed, pre_delete, post_delete)
    def test_add_fetched_keywords(self):
        """
        Verifica o funcionamento de news.add_fetched_keywords(), que deve popular
        news.keywords.
        """
        with basic_news() as news:
            self.assertIsNotNone(news._keywords)
            news.add_fetched_keywords()
            self.assertIsNotNone(news.keywords.all())
            self.assertEqual(len(news.keywords.all()), len(news._keywords))

            for fetched_keyword in news._keywords:
                self.assertIsNotNone(Keyword.objects.get(name=fetched_keyword))

    @factory.django.mute_signals(post_save, m2m_changed, pre_delete, post_delete)
    def test_add_fetched_keywords_with_preexisting_keyword(self):
        """
        Verifica o funcionamento de news.add_fetched_keywords(), que não deve
        adicionar palavras-chave repetidas.
        """
        with basic_news() as news:
            self.assertIsNotNone(news._keywords)
            self.assertIn("2015", news._keywords)
            Keyword.objects.create(name="2015")
            news.add_fetched_keywords()
            self.assertIsNotNone(news.keywords.all())
            self.assertEqual(len(news.keywords.all()), len(news._keywords))

    @factory.django.mute_signals(post_save, m2m_changed, pre_delete, post_delete)
    def test_keywords_indexing(self):
        """
        Verifica o valor de news.keywords_indexing, usado para indexação.
        """
        with basic_news() as news:
            self.assertIsNotNone(news.keywords_indexing)
            self.assertIsInstance(news.keywords_indexing, list)
            self.assertEqual(len(news.keywords_indexing), 0)

            news.add_fetched_keywords()
            self.assertEqual(len(news.keywords_indexing), len(news._keywords))

            for fetched_keyword in news._keywords:
                self.assertIn(fetched_keyword, news.keywords_indexing)

    @factory.django.mute_signals(post_save, m2m_changed, pre_delete, post_delete)
    def test_add_fetched_subjects(self):
        """
        Verifica o funcionamento de news.add_fetched_subjects(), que deve popular
        news.subjects.
        """
        with basic_news() as news:
            self.assertIsNotNone(news._subjects)
            news.add_fetched_subjects()
            self.assertIsNotNone(news.subjects.all())
            self.assertEqual(len(news.subjects.all()), len(news._subjects))

            for fetched_subject in news._subjects:
                self.assertIsNotNone(Subject.objects.get(name=fetched_subject))

    @factory.django.mute_signals(post_save, m2m_changed, pre_delete, post_delete)
    def test_add_fetched_subjects_with_preexisting_subject(self):
        """
        Verifica o funcionamento de news.add_fetched_subjects(), que não deve
        adicionar assuntos repetidos.
        """
        with basic_news() as news:
            self.assertIsNotNone(news._subjects)
            self.assertIn("Pedaladas fiscais", news._subjects)
            Subject.objects.create(name="Política Externa")
            news.add_fetched_subjects()
            self.assertIsNotNone(news.subjects.all())
            self.assertEqual(len(news.subjects.all()), len(news._subjects))

    @factory.django.mute_signals(post_save, m2m_changed, pre_delete, post_delete)
    def test_subjects_indexing(self):
        """
        Verifica o valor de news.subjects_indexing, usado para indexação.
        """
        with basic_news() as news:
            self.assertIsNotNone(news.subjects_indexing)
            self.assertIsInstance(news.subjects_indexing, list)
            self.assertEqual(len(news.subjects_indexing), 0)

            news.add_fetched_subjects()
            self.assertEqual(len(news.subjects_indexing), len(news._subjects))

            for fetched_subject in news._subjects:
                self.assertIn(fetched_subject, news.subjects_indexing)

    def test_null_field_indexing(self):
        news = News()
        self.assertIsNone(news.null_field_indexing)

    @pytest.mark.django_db(transaction=True)
    def test_has_image_and_test_add_fetched_image(self):
        """
        Verifica news.has_image.
        """
        with basic_news() as news:
            self.assertFalse(news.has_image)
            news.add_fetched_image()
            self.assertTrue(news.has_image)

    @pytest.mark.django_db(transaction=True)
    def test_add_fetched_image(self):
        """
        Verifica se news.add_fetched_image popula as propriedades
        news.image_capture, news.thumbnail e news.image_capture_indexing.
        """
        with basic_news() as news:
            with patch.object(NewsFetcher, "fetch_image") as mocked:
                with fixtures.mocked_news_add_fetched_image("abacate") as f:
                    mocked.return_value.__enter__.return_value = f
                    with self.assertRaises(
                        News.image_capture.RelatedObjectDoesNotExist
                    ):
                        news.image_capture
                    self.assertIsNone(news.thumbnail)
                    self.assertIsNone(news.image_capture_indexing)
                    news.add_fetched_image()
                    self.assertIsNotNone(news.image_capture)
                    self.assertIsInstance(news.image_capture, NewsImageCapture)
                    self.assertIsNotNone(news.thumbnail)
                    self.assertIsNotNone(news.image_capture_indexing)

    @pytest.mark.django_db(transaction=True)
    def test_add_another_fetched_image(self):
        """
        Verifica se uma captura de imagem substitui uma outra já existente
        em news.add_fetched_image().
        """
        with basic_news() as news:
            with patch.object(NewsFetcher, "fetch_image") as mocked:
                with fixtures.mocked_news_add_fetched_image("abacate") as f:
                    mocked.return_value.__enter__.return_value = f
                    news.add_fetched_image()
                    first_image_capture_pk = news.image_capture.pk
                    news.add_fetched_image()
                    self.assertNotEqual(first_image_capture_pk, news.image_capture.pk)
                    with self.assertRaises(NewsImageCapture.DoesNotExist):
                        self.assertIsNone(
                            NewsImageCapture.objects.get(pk=first_image_capture_pk)
                        )

    @pytest.mark.django_db(transaction=True)
    def test_add_fetched_image_filename_generated_with_salt(self):
        """
        Um Documento de captura de imagem não pode ter o nome de seu arquivo original deduzível a
        partir de um hash simples sem sal. Em outras palavras, a função `add_fetched_image` deve
        sempre usar um sal na geração do nome do arquivo.
        """
        with basic_news() as news:
            with patch.object(NewsFetcher, "fetch_image") as mocked:
                with fixtures.mocked_news_add_fetched_image("abacate") as f:
                    mocked.return_value.__enter__.return_value = f
                    hashed_image_filename = hashlib.md5(
                        news._image.encode("utf-8")
                    ).hexdigest()
                    news.add_fetched_image()
                    self.assertNotIn(
                        hashed_image_filename, news.image_capture.image_document.name
                    )

    @pytest.mark.django_db(transaction=True)
    def test_add_pdf_capture(self):
        """
        Verifica news.has_pdf_capture e se news.add_pdf_capture() adiciona
        outra captura de página em PDF.
        """
        with basic_news() as news:
            with patch.object(NewsFetcher, "get_pdf_capture") as mocked:
                with fixtures.mocked_news_get_pdf_capture("abacate") as f:
                    self.assertFalse(news.has_pdf_capture)
                    mocked.return_value.__enter__.return_value = f
                    news.add_pdf_capture()
                    self.assertEqual(len(news.pdf_captures.all()), 1)
                    self.assertIsInstance(news.pdf_captures.all()[0], NewsPDFCapture)
                    self.assertTrue(news.has_pdf_capture)
                    news.add_pdf_capture()
                    self.assertEqual(len(news.pdf_captures.all()), 2)
                    self.assertTrue(news.has_pdf_capture)
