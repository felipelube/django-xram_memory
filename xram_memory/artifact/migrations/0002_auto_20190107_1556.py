# Generated by Django 2.1.2 on 2019-01-07 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('artifact', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='artifact',
            name='created_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='artifact_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='artifact',
            name='modified_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='artifact_last_modifier', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='artifact',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_artifact.artifact_set+', to='contenttypes.ContentType'),
        ),
    ]
