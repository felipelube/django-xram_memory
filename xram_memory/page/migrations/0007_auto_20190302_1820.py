# Generated by Django 2.1.5 on 2019-03-02 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0006_auto_20190302_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticpage',
            name='show_in_menu',
            field=models.BooleanField(default=False, help_text='Mostrar um link para esta página no menu principal do site', verbose_name='Mostrar no menu'),
        ),
    ]
