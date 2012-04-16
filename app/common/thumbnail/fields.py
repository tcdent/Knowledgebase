from django.conf import settings
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.db import models
from django.db.models.fields import CharField
from django.db.models.fields.files import FieldFile
from django.forms import FileInput
from sorl.thumbnail.fields import ImageField, ImageFormField
from sorl.thumbnail.helpers import ThumbnailError
from sorl.thumbnail.shortcuts import get_thumbnail


# Widget
class ThumbnailInput(FileInput):
    def render(self, name, value, attrs=None):
        template = super(ThumbnailInput, self).render(name, None, attrs=attrs)
        if value:
            thumbnail = get_thumbnail(value, '100x100', crop='center')
            template = "<img src=\"%s\" width=\"100\" height=\"100\">%s" % (
                thumbnail.url, template)
        return mark_safe(template)


# Form Fields
class ThumbnailFormatter(object):
    def __init__(self, file_):
        self.file = file_
    
    def __getitem__(self, name):
        return self.get_format(name)
    
    def get_format(self, size):
        if size in settings.THUMBNAIL_FORMATS.keys():
            size = settings.THUMBNAIL_FORMATS[size]
        
        try:
            return get_thumbnail(self.file, size)
        except ThumbnailError:
            return get_thumbnail(settings.THUMBNAIL_DEFAULT, size)


class Thumbnail(FieldFile):
    def __init__(self, instance, field, name):
        super(Thumbnail, self).__init__(instance, field, name)
        self.formats = ThumbnailFormatter(self)


class ThumbnailField(ImageField):
    attr_class = Thumbnail


