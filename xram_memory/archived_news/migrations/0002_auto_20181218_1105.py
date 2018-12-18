# Generated by Django 2.1.2 on 2018-12-18 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('archived_news', '0001_initial'),
        ('taxonomy', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='archivednews',
            name='created_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='archivednews_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='archivednews',
            name='keywords',
            field=models.ManyToManyField(blank=True, to='taxonomy.Keyword', verbose_name='Palavras-chave'),
        ),
        migrations.AddField(
            model_name='archivednews',
            name='modified_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='archivednews_last_modifier', to=settings.AUTH_USER_MODEL),
        ),
    ]