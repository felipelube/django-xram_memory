# Generated by Django 2.1.7 on 2019-03-21 01:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artifact', '0001_initial'),
        ('taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newspaper',
            name='created_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='newspaper_creator', to=settings.AUTH_USER_MODEL, verbose_name='Criado por'),
        ),
        migrations.AddField(
            model_name='newspaper',
            name='modified_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='newspaper_last_modifier', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por'),
        ),
        migrations.AddField(
            model_name='newsimagecapture',
            name='image_document',
            field=filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.CASCADE, related_name='image_capture', to=settings.FILER_IMAGE_MODEL, verbose_name='Documento de imagem'),
        ),
        migrations.AddField(
            model_name='newsimagecapture',
            name='news',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image_capture', to='artifact.News', verbose_name='Notícia'),
        ),
        migrations.AddField(
            model_name='news',
            name='created_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='news_creator', to=settings.AUTH_USER_MODEL, verbose_name='Criado por'),
        ),
        migrations.AddField(
            model_name='news',
            name='keywords',
            field=models.ManyToManyField(blank=True, related_name='news', to='taxonomy.Keyword', verbose_name='Palavras-chave'),
        ),
        migrations.AddField(
            model_name='news',
            name='modified_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='news_last_modifier', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por'),
        ),
        migrations.AddField(
            model_name='news',
            name='newspaper',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news', to='artifact.Newspaper'),
        ),
        migrations.AddField(
            model_name='news',
            name='subjects',
            field=models.ManyToManyField(blank=True, related_name='news', to='taxonomy.Subject', verbose_name='Assuntos'),
        ),
    ]