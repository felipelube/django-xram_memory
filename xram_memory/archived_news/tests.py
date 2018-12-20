from django.test import TestCase, Client, TransactionTestCase
from .models import ArchivedNews, Keyword
from django.template.defaultfilters import slugify
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import ModelAdmin
from .admin import ArchivedNewsAdmin
from ..users.models import User
from django.urls import reverse
from django.db import transaction
from django.template.response import TemplateResponse
import logging

logger = logging.getLogger(__name__)

# Create your tests here.


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm):
        return True


request = MockRequest()
request.user = MockSuperUser()


class ArchivedNewsTestCase(TransactionTestCase):
    def setUp(self):
        self.archived_news = ArchivedNews(
            url="https://politica.estadao.com.br/noticias/geral,em-diplomacao-bolsonaro-diz-que-a-soberania-do-voto-popular-e-inquebrantavel,70002640605")

    def test_flags(self):
        '''Teste o estado inicial das flags'''
        self.assertEqual(self.archived_news.has_error, False)
        self.assertEqual(self.archived_news.needs_reprocessing, True)
        self.assertEqual(self.archived_news.has_basic_info, False)
        self.assertEqual(self.archived_news.has_pdf_capture, False)
        self.assertEqual(self.archived_news.has_web_archive_url, False)
        self.assertEqual(self.archived_news.is_published, False)
        self.assertEqual(self.archived_news.is_processed, False)
        self.assertEqual(self.archived_news.is_queued, False)
        self.assertEqual(self.archived_news.is_new, True)


class KeywordTestCase(TransactionTestCase):
    def setUp(self):
        with transaction.atomic():
            self.keyword = Keyword.objects.create(name="Abacate é uma fruta")

    def test_keyword_slug(self):
        '''Teste que a slug está sendo criada depois de o modelo ser salvo'''
        self.assertEqual(self.keyword.slug, slugify("Abacate é uma fruta"))


class ArchivedNewsAdminFormTestCase(TransactionTestCase):
    serialized_rollback = True

    def setUp(self):
        self.automatic_archived_news = ArchivedNews(
            url="https://politica.estadao.com.br/noticias/geral,em-diplomacao-bolsonaro-diz-que-a-soberania-do-voto-popular-e-inquebrantavel,70002640605")
        self.site = AdminSite()
        self.user_info = {
            'username': 'admin',
            'email': 'test@test.com',
            'password': 'test@test.com'
        }
        self.user = User.objects.create_superuser(**self.user_info)
        self.client = Client()
        self.client.login(**self.user_info)

    def test_fields_for_new_item(self):
        '''Testa a presença/ausência e os valores dos campos quando em modo de inserção'''
        response: TemplateResponse = self.client.get(reverse(
            "admin:archived_news_archivednews_add"))
        self.assertEqual(response.status_code, 200)

        admin_form = response.context_data['adminform']
        # Deverão existir três grupos de campos...
        self.assertEqual(len(admin_form.fieldsets), 3)
        # Um desses precisa se chamar 'Avançado'
        self.assertIn('Modo de inserção', [
                      item[0] for item in admin_form.fieldsets])
        # O campo abaixo não deverá estar presente quando esse formulário for usado para edição
        self.assertIn('insertion_mode', admin_form.form.fields)

    def test_fields_for_existing_item(self):
        '''Testa a presença/ausência e os valores dos campos quando em modo de edição'''
        self.automatic_archived_news.save()

        response: TemplateResponse = self.client.get(reverse(
            "admin:archived_news_archivednews_change", args=[self.automatic_archived_news.pk]))
        self.assertEqual(response.status_code, 200)

        admin_form = response.context_data['adminform']
        # Deverão existir três grupos de campos...
        self.assertEqual(len(admin_form.fieldsets), 3)
        # Um desses precisa se chamar 'Avançado'
        self.assertIn('Avançado', [
                      item[0] for item in admin_form.fieldsets])
        # O campo abaixo não deverá estar presente quando esse formulário for usado para edição
        self.assertNotIn('insertion_mode', admin_form.form.fields)
