# Generated by Django 2.1.7 on 2019-03-23 14:58

from django.db import migrations
import django.db.models.deletion
import filer.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ("artifact", "0004_auto_20190323_1153"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newsimagecapture",
            name="image_document",
            field=filer.fields.file.FilerFileField(
                on_delete=django.db.models.deletion.CASCADE,
                to="filer.File",
                verbose_name="Documento de imagem",
            ),
        ),
    ]
