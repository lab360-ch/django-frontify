from django import template
from django.utils.translation import ugettext_lazy as _
from django_frontify.fields import FrontifyImage

register = template.Library()


@register.simple_tag
def frontify_thumbnail(
    frontify_image: FrontifyImage,
    width=None,
    height=None,
    format=None,
    rect=None,
    reference_width=None,
):
    if not isinstance(frontify_image, FrontifyImage):
        return ""

    return frontify_image.thumbnail_url(
        width=width,
        height=height,
        format=format,
        rect=rect,
        reference_width=reference_width,
    )


@register.filter(name="frontify_metadata")
def frontify_metadata(value, arg):
    return value.metadata.get(arg, None)
