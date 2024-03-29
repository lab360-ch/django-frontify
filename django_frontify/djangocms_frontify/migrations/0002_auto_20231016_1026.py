# Generated by Django 2.2.28 on 2023-10-16 10:26

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ("djangocms_frontify", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="frontifyimagepluginmodel",
            name="format",
            field=models.CharField(
                blank=True,
                choices=[
                    (None, "auto"),
                    ("jpg", "jpg"),
                    ("jpeg", "jpeg"),
                    ("png", "png"),
                    ("webp", "webp"),
                ],
                default=getattr(
                    settings, "DJANGO_FRONTIFY_IMAGE_PLUGIN_DEFAULT_FORMAT", None
                ),
                max_length=10,
                verbose_name="Format",
            ),
        ),
    ]
