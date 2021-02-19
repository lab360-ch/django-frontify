from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from django_frontify.djangocms_frontify.models import FrontifyImagePluginModel


@plugin_pool.register_plugin
class FrontifyImagePlugin(CMSPluginBase):
    model = FrontifyImagePluginModel
    render_template = "django_frontify/plugins/image.html"
    name = _('Frontify Image')
    allow_children = False
    text_enabled = True
