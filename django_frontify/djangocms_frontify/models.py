from django.db import models
from django.conf import settings
from django.utils.translation import get_language, ugettext_lazy as _
from cms.models.pluginmodel import CMSPlugin

from django_frontify.fields import FrontifyImage, FrontifyImageField


class FrontifyImagePluginModel(CMSPlugin):
    image = FrontifyImageField(
        verbose_name=_("Image"),
    )
    width = models.PositiveIntegerField(
        verbose_name=_("Width"),
        blank=True,
        null=True,
        help_text=_(
            "The image width as number in pixels. " 'Example: "720" and not "720px".'
        ),
    )
    height = models.PositiveIntegerField(
        verbose_name=_("Height"),
        blank=True,
        null=True,
        help_text=_(
            "The image height as number in pixels. " 'Example: "720" and not "720px".'
        ),
    )
    format = models.CharField(
        verbose_name=_("Format"),
        choices=[
            (
                None,
                _("auto"),
            )
        ]
        + [(x, x) for x in FrontifyImage.SUPPORTED_FORMATS],
        default=getattr(settings, "DJANGO_FRONTIFY_IMAGE_PLUGIN_DEFAULT_FORMAT", None),
        max_length=10,
        blank=True,
    )

    @property
    def url(self):
        return self.image.thumbnail_url(
            width=self.width, height=self.height, format=self.format
        )

    @property
    def alt_text(self):
        """
        Set `DJANGO_FRONTIFY_ALT_TAG_METADATA` to get the alt text from the frontify metadata.
        If you use an `{language_code}` in the string this would be replaced by the current language code.

        E.q. alt-tag_{language_code} => alt-tag_en
        """

        return self.image.metadata.get(
            getattr(
                settings, "DJANGO_FRONTIFY_ALT_TAG_METADATA", "alt-tag_{language_code}"
            ).format(language_code=get_language()),
            "",
        )
