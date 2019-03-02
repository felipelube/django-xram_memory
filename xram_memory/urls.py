from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from xram_memory.artifact.admin.forms.news_bulk import news_bulk_insertion
from xram_memory.artifact.views import DocumentViewSet, NewsViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/artifact/news/insert_bulk', news_bulk_insertion),
]

# TODO: proteger, somente usuários autenticados
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Endpoints da API
urlpatterns = [
    path('api/v1/document/<int:pk>',
         DocumentViewSet.as_view({'get': 'retrieve'})),
    path('api/v1/news/<int:pk>',
         NewsViewSet.as_view({'get': 'retrieve'}))
] + urlpatterns


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
