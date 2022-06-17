# Generated by Django 2.1.8 on 2019-04-29 13:31

from django.db import migrations
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ("artifact", "0007_merge_20190417_0020"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="document_id",
            field=hashid_field.field.HashidField(
                alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
                help_text="Código através do qual os visitantes do site podem acessar esse documento.",
                min_length=7,
                null=True,
                verbose_name="Código do documento",
            ),
        ),
    ]
