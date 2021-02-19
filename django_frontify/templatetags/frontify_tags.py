from django import template
from django.utils.translation import ugettext_lazy as _
from django_frontify.fields import FrontifyImage

register = template.Library()


@register.simple_tag
def frontify_thumbnail(frontifyImage: FrontifyImage, width=None, height=None, format=None, rect=None, reference_width=None):
    if not isinstance(frontifyImage, FrontifyImage):
        return ""
#        raise ValueError(
#            _("first argument has to be a FrontifyImage instance."))
    return frontifyImage.thumbnail_url(width=width, height=height, format=format, rect=rect, reference_width=reference_width)
