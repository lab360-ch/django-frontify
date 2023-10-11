import json
import urllib
import logging

from typing import Optional, Literal, Tuple
from django import forms
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class FrontifyImage:
    SUPPORTED_FORMATS = [
        "jpg",
        "jpeg",
        "png",
        "webp",
    ]

    def __init__(self, data):
        data_dict = json.loads(data)
        self.metadata = {}
        for metadata in data_dict.get("metadataValues", []):
            self.metadata[metadata["metadataField"]["label"]] = metadata["value"]
        self.json_data = data

        self.name = data_dict.get("name", "")
        self.id = data_dict.get("id", "")
        self.project = data_dict.get("project", "")  # unavailable in v2
        self.creator_name = data_dict.get("creator_name", "")
        self.created = data_dict.get("created", "")
        self.modifier_name = data_dict.get("modifier_name", "")  # unavailable in v2
        self.modified = data_dict.get("modified", "")  # unavailable in v2
        self.object_type = data_dict.get("object_type", "")
        self.media_type = data_dict.get("media_type", "")  # unavailable in v2
        self.title = data_dict.get("title", "")
        self.description = data_dict.get("description", "")
        self.ext = data_dict.get("ext", "")
        self.width = data_dict.get("width", "")
        self.height = data_dict.get("height", "")
        self.filesize = data_dict.get("filesize", "")  # seems to differ in v2
        self.asset_status = data_dict.get("asset_status", "")  # unavailable in v2
        self.generic_url = data_dict.get("generic_url", "").split("?")[0]
        self.preview_url = data_dict.get("previewUrl", "")
        self.download_url = data_dict.get("download_url", "")

        if "downloadUrl" in data_dict:
            # New response when using FrontifyFinderV2
            self.ext = data_dict.get("extension", "")
            self.title = data_dict.get("title", "")
            self.name = f"{self.title}.{self.ext}"
            self.creator_name = data_dict.get("creator", {}).get("name")
            self.created = data_dict.get("createdAt", "")
            self.object_type = data_dict.get("type", "")
            self.filesize = data_dict.get("size", "")  # seems to differ in v2
            self.generic_url = data_dict.get("previewUrl", "").split("?")[0]
            self.download_url = data_dict.get("downloadUrl", "")

    @property
    def admin_preview(self):
        return self.thumbnail_url(height=36)

    def __str__(self):
        return self.json_data

    def thumbnail_url(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        format: Optional[str] = None,
        quality: Optional[int] = None,
        fp: Optional[Tuple[float, float]] = None,
        crop: Literal["fp"] = None,
        fp_zoom: Optional[float] = None,
        rect=None,
        reference_width=None,
    ):
        """
        https://developer.frontify.com/d/XFPCrGNrXQQM/asset-processing-api
        """
        if rect is not None or reference_width is not None:
            logging.warn(
                """\n
The attributes `rect` and `reference_with` are no longer used.
Please use `crop=\"fp\"` and `fp=(0.5,0.5)` instead.
More detailed information can be found here: https://developer.frontify.com/d/XFPCrGNrXQQM/asset-processing-api#/operations/cropping-focal-point
            \n"""
            )
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
        if format:
            if format not in FrontifyImage.SUPPORTED_FORMATS:
                raise ValueError(
                    _(
                        f"{format} is not a allowed format. Allowed formats are {','.join(FrontifyImage.SUPPORTED_FORMATS)}"
                    )
                )
            params.append(("format", format))
        if quality is not None:
            try:
                quality = int(quality)
            except ValueError:
                raise ValueError(
                    _(
                        f"quality has to be an int between 0 and 100. `{quality}` is not a valid value"
                    )
                )
            else:
                if quality > 100 or quality < 0:
                    raise ValueError(
                        _(
                            f"quality has to be an int between 0 and 100. `{quality}` is not a valid value"
                        )
                    )
                params.append(("quality", quality))

        if crop is not None:
            if crop == "fp":
                params.append(("crop", crop))
                if fp is None:
                    params.append(("fp", "0.5,0.5"))
                try:
                    (x, y) = fp
                except TypeError:
                    raise ValueError(
                        "The argument `fp` must be a tuple of two floats between 0.0 and 1.0"
                    )
                if x > 1.0 or x < 0.0 or y > 1.0 or y < 0.0:
                    raise ValueError(
                        "The argument `fp` must be a tuple of two floats between 0.0 and 1.0"
                    )
                params.append(("fp", f"{x},{y}"))
                if fp_zoom is not None:
                    try:
                        fp_zoom = float(fp_zoom)
                    except ValueError:
                        raise ValueError(
                            "The argument `fp_zoom` need to be a float between 1.0 and 3.0"
                        )
                    if fp_zoom > 3.0 or fp_zoom < 1.0:
                        raise ValueError(
                            "The argument `fp_zoom` need to be a float between 1.0 and 3.0"
                        )
                    params.append(("fp_zoom", fp_zoom))
            else:
                raise ValueError(
                    _("Only `fp` as value for the crop argument is allowed.")
                )

        return "{}?{}".format(self.generic_url, urllib.parse.urlencode(params))


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
            "client_id": getattr(settings, "DJANGO_FRONTIFY_CLIENT_ID", ""),
            "finder_version": getattr(settings, "DJANGO_FRONTIFY_FINDER_VERSION", 2),
            **attrs,
        }
        html = render_to_string(
            "admin/django_frontify/widgets/admin_file.html", context
        )
        return mark_safe(html)

    class Media(object):
        css = {"all": ["django_frontify/widget.css"]}
        if getattr(settings, "DJANGO_FRONTIFY_FINDER_VERSION", 2) == 2:
            js = (
                "https://unpkg.com/@frontify/frontify-finder@2.0.1/dist/index.js",
                "django_frontify/widget.js",
            )
        else:
            js = (
                "https://cdn.frontify.com/finder/frontify-finder-latest.min.js",
                "django_frontify/widget.js",
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
        kwargs.update({"form_class": AdminFrontifyFormField})
        return super().formfield(**kwargs)
