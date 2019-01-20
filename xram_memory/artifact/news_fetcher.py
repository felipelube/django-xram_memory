import requests
import pdfkit

from newspaper import Article
from goose3 import Goose
from goose3.image import Image
from functools import lru_cache


class NewsFetcher:
    @staticmethod
    def fetch_archived_url(url):
        '''
        Verifica se existe adiciona a URL de uma versão arquivada desta notícia no `Internet Archive`
        '''
        response = requests.get(
            "https://archive.org/wayback/available?url={}".format(url))
        response.raise_for_status()
        response = response.json()

        if (response["archived_snapshots"] and response["archived_snapshots"]["closest"] and
                response["archived_snapshots"]["closest"]["available"]):
            closest_archive = response["archived_snapshots"]["closest"]
            return closest_archive["url"]
        return ''

    @staticmethod
    def get_pdf_capture(url, pdf_dir):
        """
        Captura a notícia em formato para impressão e em PDF
        """

        # TODO: checar se o diretório existe, se existem permissões para salvar etc
        # TODO: usar o System check framework
        if not pdf_dir:
            raise ValueError(
                'NewsFetcher: o caminho para onde salvar as páginas não foi definido')

        return pdfkit.from_url(url, False, options={
            'print-media-type': None,
            'disable-javascript': None,
        })

    @staticmethod
    def fetch_image(image_url):
        response = requests.get(image_url, allow_redirects=True)
        response.raise_for_status()
        return response.content

    @staticmethod
    @lru_cache(maxsize=2)
    def fetch_basic_info(url):
        '''
        Dada uma URL, extraia informações básicas sobre uma notícia usando as bibliotecas newspaper3k e goose
        '''
        # Tente extrair primeiro usando o newspaper3k e reutilize seu html, se possível
        newspaper_article = NewsFetcher._extract_using_newspaper(url)
        if newspaper_article:
            goose_article = NewsFetcher._extract_using_goose3(
                url, newspaper_article.html)
        else:
            goose_article = NewsFetcher._extract_using_goose3(url)
        if newspaper_article is None and goose_article is None:
            raise(Exception(
                'Não foi possível extrair informações básicas sobre a notícia, pois nenhum dos extratores funcionou.'))
        basic_info = NewsFetcher._merge_extractions(
            newspaper_article, goose_article)
        # TODO: remover stopwords de basic_info['keywords']
        return basic_info

    @staticmethod
    def _merge_extractions(newspaper_article, goose_article):
        '''
        Com base nas extrações passadas, constrói um dicionário em que a informação de cada uma é aproveitada, se existir.
        '''
        def join_with_comma(list):
            return ",".join(list)

        try:
            # TODO: melhorar esse código, que está safo, mas feio pra caramba
            news_dict = {
                'title': newspaper_article.title if getattr(newspaper_article, 'title', None) else getattr(goose_article, 'title', None),
                'image': newspaper_article.top_image if getattr(newspaper_article, 'top_image', None) else goose_article.top_image.src if isinstance(getattr(goose_article, 'top_image', None), Image) else None,
                'body': newspaper_article.text if getattr(newspaper_article, 'text', None) else getattr(goose_article, 'cleaned_text', None),
                'teaser': getattr(newspaper_article, 'summary', None),

                'published_date': newspaper_article.publish_date if getattr(newspaper_article, 'publish_date', None) else getattr(goose_article, 'publish_date', None),

                'authors': join_with_comma(newspaper_article.authors if getattr(newspaper_article, 'authors', []) else getattr(goose_article, 'authors', [])),
                'keywords': newspaper_article.keywords if getattr(newspaper_article, 'keywords', []) else getattr(goose_article, 'tags', []),
            }
            return news_dict
        except Exception as err:
            raise(
                Exception(
                    "Falha ao construir o dicionário com as informações básicas da notícia: {}."
                    .format(str(err))
                )
            )

    @staticmethod
    def _extract_using_newspaper(url, raw_html=None):
        """
        Tenta extrair usando a biblioteca newspaper3k
        """
        try:
            newspaper_article = Article(url)

            if raw_html:
                newspaper_article.download(input_html=raw_html)
            else:
                newspaper_article.download()
            newspaper_article.parse()
            newspaper_article.nlp()

            return newspaper_article
        except:
            return None

    @staticmethod
    def _extract_using_goose3(url, raw_html=None):
        """
        Tenta extrair usando a biblioteca goose3
        """
        try:
            goose = Goose({'enable_image_fetching': True})

            if raw_html:
                goose_article = goose.extract(raw_html=raw_html, url=url)
            else:
                goose_article = goose.extract(url=url)

            return goose_article
        except:
            return None
