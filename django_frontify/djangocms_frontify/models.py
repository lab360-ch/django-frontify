from django.db import models
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from django_frontify.fields import FrontifyImage, FrontifyImageField


class FrontifyImagePluginModel(CMSPlugin):
    image = FrontifyImageField(
        verbose_name=_('Image'),
    )
    width = models.PositiveIntegerField(
        verbose_name=_('Width'),
        blank=True,
        null=True,
        help_text=_(
            'The image width as number in pixels. '
            'Example: "720" and not "720px".'
        ),
    )
    height = models.PositiveIntegerField(
        verbose_name=_('Height'),
        blank=True,
        null=True,
        help_text=_(
            'The image height as number in pixels. '
            'Example: "720" and not "720px".'
        ),
    )
    format = models.CharField(
        verbose_name=_("Format"),
        choices=[
            (None, _("auto"),)
        ]+[
            (x, x) for x in FrontifyImage.SUPPORTED_FORMATS
        ],
        max_length=10,
        blank=True,

    )

    @property
    def url(self):
        return self.image.thumbnail_url(width=self.width, height=self.height, format=self.format)
