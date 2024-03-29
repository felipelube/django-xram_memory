from django.conf import settings
from django_elasticsearch_dsl import DocType, Index, fields
from xram_memory.artifact.models import (
    News,
    NewsPDFCapture,
    NewsImageCapture,
    Newspaper,
)
from xram_memory.taxonomy.models import Keyword, Subject

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1,
    blocks={"read_only_allow_delete": False},
    # read_only_allow_delete=False,
    analysis={
        "filter": {
            "portuguese_stop": {"type": "stop", "stopwords": "_portuguese_"},
            "portuguese_stemmer": {"type": "stemmer", "language": "light_portuguese"},
            "snowball_portuguese": {"type": "snowball", "language": "portuguese"},
        },
        "analyzer": {
            "rebuilt_portuguese": {
                "tokenizer": "standard",
                "filter": ["lowercase", "portuguese_stop", "portuguese_stemmer"],
            },
            "html_strip": {
                "tokenizer": "standard",
                "filter": ["standard", "lowercase", "stop", "snowball"],
                "char_filter": ["html_strip"],
            },
        },
        "normalizer": {
            "my_normalizer": {
                "type": "custom",
                "char_filter": [],
                "filter": ["lowercase", "asciifolding"],
            }
        },
    },
)


# TODO: indexar apenas notícias publicadas
@INDEX.doc_type
class NewsDocument(DocType):
    """
    Índice de pesquisa para o modelo News
    """

    # Campos comuns
    id = fields.IntegerField(attr="id")
    created_at = fields.DateField()
    modified_at = fields.DateField()
    title = fields.TextField(
        analyzer="rebuilt_portuguese", fields={"raw": fields.KeywordField()}
    )
    teaser = fields.TextField(analyzer="rebuilt_portuguese")
    keywords = fields.NestedField(
        properties={"name": fields.KeywordField(), "slug": fields.KeywordField()}
    )
    subjects = fields.NestedField(
        properties={"name": fields.KeywordField(), "slug": fields.KeywordField()}
    )
    thumbnail = fields.KeywordField(attr="thumbnail")
    published_year = fields.IntegerField(attr="published_year")
    # Campos específicos
    url = fields.KeywordField()
    published = fields.BooleanField()
    featured = fields.BooleanField()
    pdf_captures = fields.NestedField(
        properties={
            "pdf_document": fields.NestedField(
                properties={
                    "id": fields.IntegerField(index=False),
                    "size": fields.IntegerField(index=False),
                }
            ),
            "pdf_capture_date": fields.DateField(index=False),
        }
    )
    slug = fields.KeywordField()
    published_date = fields.DateField()
    language = fields.KeywordField()
    newspaper = fields.NestedField(
        properties={
            "url": fields.KeywordField(),
            "title": fields.KeywordField(),
            "favicon_logo": fields.KeywordField(attr="favicon_logo"),
        }
    )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Keyword):
            return related_instance.news.all()
        elif isinstance(related_instance, Subject):
            return related_instance.news.all()
        elif isinstance(related_instance, Newspaper):
            return related_instance.news.all()
        elif isinstance(related_instance, NewsImageCapture):
            return related_instance.news
        elif isinstance(related_instance, NewsPDFCapture):
            return related_instance.news

    class Meta(object):
        model = News  # O modelo associado a este documento
        parallel_indexing = True
        doc_type = "Notícia"
        related_models = [Keyword, Subject, NewsPDFCapture, NewsImageCapture, Newspaper]
