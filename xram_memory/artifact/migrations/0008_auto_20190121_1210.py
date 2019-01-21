# Generated by Django 2.1.2 on 2019-01-21 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0007_auto_20190120_2245'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsimagecapture',
            options={'verbose_name': 'Imagem de Notícia', 'verbose_name_plural': 'Imagens de Notícias'},
        ),
        migrations.AlterField(
            model_name='document',
            name='teaser',
            field=models.TextField(blank=True, help_text='Resumo ou chamada', null=True, verbose_name='Resumo ou chamada'),
        ),
        migrations.AlterField(
            model_name='news',
            name='teaser',
            field=models.TextField(blank=True, help_text='Resumo ou chamada', null=True, verbose_name='Resumo ou chamada'),
        ),
        migrations.AlterField(
            model_name='newsimagecapture',
            name='image_document',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='artifact.ImageDocument', verbose_name='Documento de imagem'),
        ),
        migrations.AlterField(
            model_name='newsimagecapture',
            name='news',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='image_capture', to='artifact.News', verbose_name='Notícia'),
        ),
        migrations.AlterField(
            model_name='newsimagecapture',
            name='original_url',
            field=models.CharField(max_length=255, unique=True, verbose_name='Endereço original da imagem'),
        ),
        migrations.AlterField(
            model_name='newspdfcapture',
            name='news',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pdf_captures', to='artifact.News', verbose_name='Notícia'),
        ),
        migrations.AlterField(
            model_name='newspdfcapture',
            name='pdf_document',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='artifact.PDFDocument', verbose_name='Documento PDF'),
        ),
    ]
