from .fixtures import (NEWS_ITEMS, VALID_NEWS_URL, BlankPlugin, FunctionalPlugin,
                       NonFunctionalPlugin, news_fetcher_plugin_factory)
from xram_memory.lib.news_fetcher.plugins.base import (
    ArchivePluginBase, PDFCapturePluginBase, BasicInfoPluginBase)
from xram_memory.lib.news_fetcher import NewsFetcher
from django.core.exceptions import ValidationError
from contextlib import contextmanager
from django.utils.timezone import now
from django.test import TestCase
import pytest

"""
TODO: criar gerenciador de contexto ou decorador que permita definir
temporariamente os plugins num registro de plugins.
Da forma como os testes estão implementados, há pouluição no registro de
plugins, ou seja, outros testes podem falhar se esperarem que esse registro
esteja populado com plugins reais não mockados.
"""


def test_function_with_invalid_urls():
    """
    Testa o validador de urls em todas funções que aceitam uma url
    """
    functions_that_accept_url = (NewsFetcher.fetch_archived_url, NewsFetcher.fetch_basic_info,
                             NewsFetcher.fetch_web_title, NewsFetcher.get_pdf_capture,
                             NewsFetcher.fetch_image, NewsFetcher.build_newspaper,)
    for function in functions_that_accept_url:
        with pytest.raises(ValidationError) as f:
            with function('invalid_url'):
                pass


################################%##
# Testes com fetch_archived_url() #
##################################%

def test_fetch_archived_url_with_valid_url(news_fetcher_plugin_factory):
    """
    Testa o plugin mockado FunctionalPlugin
    """
    ArchivePluginBase.plugins = news_fetcher_plugin_factory()
    url = NewsFetcher.fetch_archived_url(VALID_NEWS_URL)
    assert url == 'OK'


def test_fetch_archived_url_with_no_plugins():
    """
    Um erro deve ser levantado quisermos usar a funcionalidade
    sem plugins registrados
    """
    ArchivePluginBase.plugins = []
    with pytest.raises(RuntimeError) as f:
        NewsFetcher.fetch_archived_url(VALID_NEWS_URL)
    assert 'Nenhum' in f.value.args[0]


def test_fetch_archived_url_with_blank_plugin(news_fetcher_plugin_factory):
    """
    Testa o plugin mockado BlankPlugin
    """
    ArchivePluginBase.plugins = news_fetcher_plugin_factory([BlankPlugin])
    url = NewsFetcher.fetch_archived_url(VALID_NEWS_URL)
    assert url == ''


def test_fetch_archived_url_with_blank_plugin_failed_plugin(news_fetcher_plugin_factory):
    """
    Testa a exceção lançada no caso de plugins sem resultado e com falha
    """
    ArchivePluginBase.plugins = news_fetcher_plugin_factory([
        BlankPlugin, NonFunctionalPlugin])
    with pytest.raises(RuntimeError) as f:
        NewsFetcher.fetch_archived_url(VALID_NEWS_URL)
    assert 'plugins falharam' in f.value.args[0]


def test_fetch_archived_url_with_blank_failed_functional_plugin(news_fetcher_plugin_factory):
    """
    Testa o comportamento no caso de ao menos um plugin funcional
    """
    ArchivePluginBase.plugins = news_fetcher_plugin_factory([FunctionalPlugin,
                                                             BlankPlugin,
                                                             NonFunctionalPlugin])
    url = NewsFetcher.fetch_archived_url(VALID_NEWS_URL)
    assert url == 'OK'

################################
# Testes com get_pdf_capture() #
################################

def test_get_pdf_capture_with_valid_url(news_fetcher_plugin_factory):
    """
    Testa o plugin mockado FunctionalPlugin
    """
    PDFCapturePluginBase.plugins = news_fetcher_plugin_factory(
        [FunctionalPlugin])
    with NewsFetcher.get_pdf_capture(VALID_NEWS_URL) as f:
        assert f == 'OK'


def test_get_pdf_capture_with_no_plugins():
    """
    Um erro deve ser levantado quisermos usar a funcionalidade
    sem plugins registrados
    """
    PDFCapturePluginBase.plugins = []
    with pytest.raises(RuntimeError) as f:
        with NewsFetcher.get_pdf_capture(VALID_NEWS_URL) as f:
            pass
    assert 'Nenhum' in f.value.args[0]


def test_get_pdf_capture_with_non_functional_plugin(news_fetcher_plugin_factory):
    """
    Testa a exceção lançada no caso de plugins com falha
    """
    PDFCapturePluginBase.plugins = news_fetcher_plugin_factory(
        [NonFunctionalPlugin])
    with pytest.raises(RuntimeError) as f:
        with NewsFetcher.get_pdf_capture(VALID_NEWS_URL) as f:
            pass
    assert 'alguns plugins falharam' in f.value.args[0]

#################################
# Testes com fetch_basic_info() #
#################################


def test_fetch_basic_info_with_valid_url(news_fetcher_plugin_factory):
    BasicInfoPluginBase.plugins = news_fetcher_plugin_factory(
        [FunctionalPlugin])
    NewsFetcher.fetch_basic_info.cache_clear()
    url = NewsFetcher.fetch_basic_info(VALID_NEWS_URL)
    assert url in [NEWS_ITEMS[1], NEWS_ITEMS[0]]


def test_fetch_basic_info_with_no_plugins():
    """
    Um erro deve ser levantado quisermos usar a funcionalidade
    sem plugins registrados
    """
    BasicInfoPluginBase.plugins = []
    with pytest.raises(RuntimeError) as f:
        NewsFetcher.fetch_basic_info.cache_clear()
        NewsFetcher.fetch_basic_info(VALID_NEWS_URL)
    assert 'Nenhum' in f.value.args[0]


def test_fetch_basic_info_with_blank_plugin(news_fetcher_plugin_factory):
    """
    Um erro deve ser levantado todos os plugins
    retornarem resultado em branco
    """
    BasicInfoPluginBase.plugins = news_fetcher_plugin_factory([BlankPlugin])

    with pytest.raises(RuntimeError) as f:
        NewsFetcher.fetch_basic_info.cache_clear()
        NewsFetcher.fetch_basic_info(VALID_NEWS_URL)
    assert 'nenhum plugin' in f.value.args[0]


def test_fetch_basic_info_with_blank_plugin_failed_plugin(news_fetcher_plugin_factory):
    """
    Testa a exceção lançada no caso de plugins com falha
    """
    BasicInfoPluginBase.plugins = news_fetcher_plugin_factory([
        BlankPlugin, NonFunctionalPlugin])
    with pytest.raises(RuntimeError) as f:
        NewsFetcher.fetch_basic_info.cache_clear()
        NewsFetcher.fetch_basic_info(VALID_NEWS_URL)
    assert 'plugins falharam' in f.value.args[0]


def test_fetch_basic_info_with_blank_failed_functional_plugin(news_fetcher_plugin_factory):
    """
    Testa o comportamento no caso de ao menos um plugin funcional
    """
    BasicInfoPluginBase.plugins = news_fetcher_plugin_factory([FunctionalPlugin,
                                                               BlankPlugin,
                                                               NonFunctionalPlugin])
    NewsFetcher.fetch_basic_info.cache_clear()
    url = NewsFetcher.fetch_basic_info(VALID_NEWS_URL)
    assert url in [NEWS_ITEMS[1], NEWS_ITEMS[0]]


def test_fetch_basic_info_conservative_nature(news_fetcher_plugin_factory):
    """
    Testa o comportamento 'conservador' no tratamento dos campos 'keywords' e
    'subjects', ou seja, o máximo de itens não repetidos deve ser obtido de
    todos os plugins registrados
    """
    BasicInfoPluginBase.plugins = news_fetcher_plugin_factory([FunctionalPlugin,
                                                               NonFunctionalPlugin])
    BasicInfoPluginBase.plugins[0].parse = lambda url, html: NEWS_ITEMS[0]
    BasicInfoPluginBase.plugins[1].parse = lambda url, html: NEWS_ITEMS[1]
    NewsFetcher.fetch_basic_info.cache_clear()
    url = NewsFetcher.fetch_basic_info(VALID_NEWS_URL)
    for key in BasicInfoPluginBase.BASIC_EMPTY_INFO.keys():
        if key in ('keywords', 'subjects'):
            continue
        assert url[key] == NEWS_ITEMS[0][key]
    assert url['keywords'] == NEWS_ITEMS[0]['keywords'] + \
        NEWS_ITEMS[1]['keywords']
    assert url['subjects'] == NEWS_ITEMS[0]['subjects'] + \
        NEWS_ITEMS[1]['subjects']
