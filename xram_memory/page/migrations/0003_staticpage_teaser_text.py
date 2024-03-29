# Generated by Django 2.1.8 on 2019-05-30 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("page", "0002_auto_20190321_2252"),
    ]

    operations = [
        migrations.AddField(
            model_name="staticpage",
            name="teaser_text",
            field=models.CharField(
                blank=True,
                help_text="Texto que será exibido como link para esta página na página inicial",
                max_length=255,
                null=True,
                verbose_name="Texto do link de chamada",
            ),
        ),
    ]
