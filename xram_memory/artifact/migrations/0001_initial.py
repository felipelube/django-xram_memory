# Generated by Django 2.1.7 on 2019-03-19 15:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields
import xram_memory.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filer', '0010_auto_20180414_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('file_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='filer.File')),
                ('mime_type', models.CharField(blank=True, editable=False, help_text='Tipo do arquivo', max_length=255, verbose_name='Tipo')),
                ('is_user_object', models.BooleanField(default=True, editable=False, help_text='Indica se o arquivo foi inserido diretamente por um usuário', verbose_name='Objeto criado pelo usuário?')),
            ],
            options={
                'verbose_name': 'Documento',
                'verbose_name_plural': 'Documentos',
            },
            bases=('filer.file',),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('published', models.BooleanField(default=True, verbose_name='Publicado?')),
                ('featured', models.BooleanField(default=True, verbose_name='Em destaque na página inicial?')),
                ('title', models.CharField(blank=True, help_text='Título', max_length=255, verbose_name='Título')),
                ('teaser', models.TextField(blank=True, help_text='Resumo ou chamada', null=True, verbose_name='Resumo ou chamada')),
                ('slug', models.SlugField(blank=True, verbose_name='Slug')),
                ('url', models.URLField(help_text='Endereço original da notícia', max_length=255, unique=True, validators=[django.core.validators.URLValidator], verbose_name='Endereço')),
                ('archived_news_url', models.URLField(blank=True, help_text="Endereço da notícia no <a href='https://archive.org/'>Archive.org</a>", max_length=255, null=True, verbose_name='Endereço no Internet Archive')),
                ('authors', models.TextField(blank=True, help_text='Nomes dos autores, separados por vírgula', verbose_name='Autores')),
                ('body', models.TextField(blank=True, help_text='Texto integral da notícia', null=True, verbose_name='Texto da notícia')),
                ('published_date', models.DateTimeField(blank=True, help_text='Data em que a notícia foi publicada', null=True, verbose_name='Data de publicação')),
                ('language', models.CharField(blank=True, default='pt', max_length=2, null=True)),
            ],
            options={
                'verbose_name': 'Notícia',
                'verbose_name_plural': 'Notícias',
            },
        ),
        migrations.CreateModel(
            name='NewsImageCapture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_capture_date', models.DateTimeField(auto_now_add=True, help_text='Data desta captura', null=True, verbose_name='Data de captura')),
                ('original_url', models.CharField(max_length=255, verbose_name='Endereço original da imagem')),
            ],
            options={
                'verbose_name': 'Imagem de Notícia',
                'verbose_name_plural': 'Imagens de Notícias',
            },
        ),
        migrations.CreateModel(
            name='Newspaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('published', models.BooleanField(default=True, verbose_name='Publicado?')),
                ('featured', models.BooleanField(default=True, verbose_name='Em destaque na página inicial?')),
                ('title', models.CharField(blank=True, help_text='Título', max_length=255, verbose_name='Título')),
                ('slug', models.SlugField(blank=True, verbose_name='Slug')),
                ('url', models.URLField(help_text='Endereço do site', max_length=255, unique=True, validators=[django.core.validators.URLValidator], verbose_name='Endereço')),
                ('description', models.TextField(blank=True, help_text='A descrição desse veículo/site', verbose_name='Descrição')),
                ('logo', easy_thumbnails.fields.ThumbnailerField(blank=True, upload_to='news_sources_logos', validators=[xram_memory.utils.FileValidator(content_types=('image/jpeg', 'image/png', 'image/gif', 'image/webp'))], verbose_name='Logotipo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NewsPDFCapture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_capture_date', models.DateTimeField(auto_now_add=True, help_text='Data desta captura', null=True, verbose_name='Data de captura')),
                ('news', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pdf_captures', to='artifact.News', verbose_name='Notícia')),
                ('pdf_document', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='artifact.Document', verbose_name='Documento PDF')),
            ],
            options={
                'verbose_name': 'Captura de Notícia em PDF',
                'verbose_name_plural': 'Capturas de Notícia em PDF',
            },
        ),
    ]
