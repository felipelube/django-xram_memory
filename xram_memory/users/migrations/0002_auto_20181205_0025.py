# Generated by Django 2.1.2 on 2018-12-05 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(
                blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
