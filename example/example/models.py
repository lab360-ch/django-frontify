from django.db import models

from django_frontify.fields import FrontifyImageField


class ExampleImageModel(models.Model):
    frontify_image = FrontifyImageField(
        verbose_name="Frontify Image",
        blank=True
    )
