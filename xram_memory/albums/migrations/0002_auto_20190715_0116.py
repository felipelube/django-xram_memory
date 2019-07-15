# Generated by Django 2.1.10 on 2019-07-15 04:16

from django.db import migrations, models
import django.db.models.deletion
import filer.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0010_auto_20180414_2058'),
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'verbose_name': 'Álbuns de fotos'},
        ),
        migrations.AddField(
            model_name='album',
            name='cover',
            field=filer.fields.file.FilerFileField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='album_cover', to='filer.File'),
        ),
        migrations.AddField(
            model_name='album',
            name='description',
            field=models.TextField(blank=True, help_text='Uma descrição detalhada para este Assunto', verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='album',
            name='featured',
            field=models.BooleanField(default=True, verbose_name='Em destaque na página de álbums'),
        ),
    ]
