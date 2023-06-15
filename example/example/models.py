from django.db import models

from django_frontify.fields import FrontifyImageField


class ExampleImageModel(models.Model):
    frontify_image = FrontifyImageField(verbose_name="Frontify Image", blank=True)

    def cropped_image(self):
        return self.frontify_image.thumbnail_url(
            width=500,
            height=500,
            rect=[0, 0, 10, 10],
            quality=100,
            format="png",
            crop="fp",
            fp=(1.0, 0.0),
            fp_zoom="1.5",
        )
