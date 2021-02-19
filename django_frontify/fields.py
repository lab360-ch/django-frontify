import json
import urllib

from django import forms
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class FrontifyImage:
    SUPPORTED_FORMATS = ["jpg", "jpeg", "png"]

    def __init__(self, data):
        data_dict = json.loads(data)
        self.json_data = data
        self.name = data_dict.get("name", "")
        self.id = data_dict.get("id", "")
        self.project = data_dict.get("project", "")
        self.creator_name = data_dict.get("creator_name", "")
        self.created = data_dict.get("created", "")
        self.modifier_name = data_dict.get("modifier_name", "")
        self.modified = data_dict.get("modified", "")
        self.object_type = data_dict.get("object_type", "")
        self.media_type = data_dict.get("media_type", "")
        self.title = data_dict.get("title", "")
        self.description = data_dict.get("description", "")
        self.ext = data_dict.get("ext", "")
        self.width = data_dict.get("width", "")
        self.height = data_dict.get("height", "")
        self.filesize = data_dict.get("filesize", "")
        self.asset_status = data_dict.get("asset_status", "")
        self.generic_url = data_dict.get("generic_url", "").split("?")[0]
        self.preview_url = data_dict.get("preview_url", "")
        self.download_url = data_dict.get("download_url", "")

    @property
    def admin_preview(self):
        return self.thumbnail_url(height=36)

    def __str__(self):
        return self.json_data

    def thumbnail_url(self, width=None, height=None, format=None, rect=None, reference_width=None):
        """
            width (Integer, px), height (Integer, px): 
                diese werden verwendet um das bild zu skalieren. Dabei wird kein cropping eingesetzt.
                Dies bedeuted, dass das Bild so skaliert wird, dass es in dieses Frame passt.
                Es müssen nicht beide gegeben sein.
                    Example: https://.../asdkebfuef&width=400
                    Example: https://.../asdkebfuef&width=400&height=800
            format (string, jpg, jpeg, png): 
                Das format des Bildes. Standardmäßig entweder png (für png, tiff, dng, ...), jpg (für jpg)
                    Example: https://.../asdkebfuef&format=jpg
                    Example: https://.../asdkebfuef&format=png
            rect (Array, kommagetrennt Integer[], [offsetX, offsetY, width, height]) & reference_width (Integer):
                Dieses wird verwendet um ein Bild auf einen Ausschnitt zu beschneiden (cropping).
                Diese Werte werden relativ zur gegebenen reference_width auf das Original angewendet.
                Das bedeutet, wenn das Bild im cropper 1000px breit ist, so können OffsetX / Y und Dimensionen
                übernommen werden und als Referenz 1000px übergeben werden. 
                Des weiteren wichtig: Wird zusätzlich ein width (or and height) Parameter übergeben,
                wird anschliessend das beschnittene Resultat zusätzlich skaliert.

            Ausblick: Da der Rect Parameter nicht so intuitiv ist,
            werden zur Zeit neue Optionen die mit Prozentangaben funktionieren entwickelt.
            Zusäzlich dazu sind wir an der Implementation des Focal Point cropping.
            Diese Funktionen sollten ende Q4 Anfang Q1 2021 bereit sein und in der neuen Dokumentation enthalten sein.
        """
        params = []
        if width is not None:
            if isinstance(width, str):
                width = int(width)
            if not isinstance(width, int):
                raise ValueError(_("width has to be a int or int as str"))
            params.append(("width", width))
        if height is not None:
            if isinstance(height, str):
                height = int(height)
            if not isinstance(height, int):
                raise ValueError(_("height has to be a int or int as str"))
            params.append(("height", height))
        if reference_width is not None:
            if isinstance(reference_width, str):
                reference_width = int(reference_width)
            if not isinstance(reference_width, int):
                raise ValueError(
                    _("reference_width has to be a int or int as str"))
            params.append(("reference_width", reference_width))
        if format:
            if format not in FrontifyImage.SUPPORTED_FORMATS:
                raise ValueError(
                    _(f"{format} is not a allowed format. Allowed formats are {','.join(FrontifyImage.SUPPORTED_FORMATS)}"))
            params.append(("format", format))
        if rect is not None:
            if isinstance(rect, str):
                rect = [int(x) for x in rect.split(",")]
            if not isinstance(rect, list) or len(rect) != 4:
                raise ValueError(
                    _("rect has to be a list of four values or a string of four comma separated numbers"))
            params.append(("rect", rect))

        return "{}?{}".format(
            self.generic_url,
            urllib.parse.urlencode(params)
        )


def convert_to_frontify_image_instance(value):
    if isinstance(value, FrontifyImage) or value is None:
        return value
    if not value:
        return None
    return FrontifyImage(value)


class AdminFrontifyWidget(forms.Textarea):
    def render(self, name, value, attrs=None, renderer=None):
        hidden_input = super().render(name, value, attrs=attrs, renderer=renderer)
        instance = convert_to_frontify_image_instance(value)
        context = {
            "instance": instance,
            "hidden_input": hidden_input,
            "domain": settings.DJANGO_FRONTIFY_DOMAIN,
            ** attrs
        }
        html = render_to_string(
            'admin/django_frontify/widgets/admin_file.html',
            context
        )
        return mark_safe(html)

    class Media(object):
        css = {
            'all': [
                'django_frontify/widget.css'
            ]
        }
        js = (
            'https://cdn.frontify.com/finder/frontify-finder-latest.min.js',
            'django_frontify/widget.js',
        )


class AdminFrontifyFormField(forms.CharField):
    widget = AdminFrontifyWidget


class FrontifyImageField(models.Field):
    description = _("Text")

    def _parse_string(self, value):
        return convert_to_frontify_image_instance(value)

    def get_internal_type(self):
        return "TextField"

    def to_python(self, value):
        return self._parse_string(value)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        """
        Return field's value prepared for interacting with the database backend.

        Used by the default implementations of get_db_prep_save().
        """
        if not prepared and isinstance(value, FrontifyImage):
            return value.json_data
        return value

    def from_db_value(self, value, expression, connection):
        return self._parse_string(value)

    def formfield(self, **kwargs):
        kwargs.update({
            "form_class": AdminFrontifyFormField
        })
        return super().formfield(**kwargs)
