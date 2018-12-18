# Generated by Django 2.1.2 on 2018-12-18 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_auto_20181218_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivednewspdfcapture',
            name='url_of_capture',
            field=models.URLField(blank=True, editable=False, help_text='Endereço original da notícia que gerou essa captura', max_length=255, null=True, unique=True, verbose_name='Endereço'),
        ),
    ]
