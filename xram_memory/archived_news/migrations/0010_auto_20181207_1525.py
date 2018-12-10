# Generated by Django 2.1.2 on 2018-12-07 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archived_news', '0009_auto_20181207_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivednews',
            name='images',
            field=models.TextField(
                blank=True, editable=False, verbose_name='Imagens'),
        ),
        migrations.AlterField(
            model_name='archivednews',
            name='summary',
            field=models.TextField(
                blank=True, verbose_name='Resumo da notícia'),
        ),
        migrations.AlterField(
            model_name='archivednews',
            name='top_image',
            field=models.ImageField(
                blank=True, upload_to='', verbose_name='Imagem principal'),
        ),
    ]