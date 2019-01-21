# Generated by Django 2.1.2 on 2019-01-21 00:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0005_auto_20190120_1653'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagedocument',
            old_name='image_file',
            new_name='file',
        ),
        migrations.RenameField(
            model_name='pdfdocument',
            old_name='pdf_file',
            new_name='file',
        ),
        migrations.RemoveField(
            model_name='document',
            name='additional_info',
        ),
        migrations.RemoveField(
            model_name='document',
            name='file_hash',
        ),
        migrations.AlterField(
            model_name='document',
            name='is_user_object',
            field=models.BooleanField(default=True, editable=False, help_text='Indica se o arquivo foi inserido diretamente por um usuário', verbose_name='Objeto criado pelo usuário?'),
        ),
        migrations.AlterField(
            model_name='news',
            name='url',
            field=models.URLField(help_text='Endereço original da notícia', max_length=255, unique=True, validators=[django.core.validators.URLValidator], verbose_name='Endereço'),
        ),
    ]