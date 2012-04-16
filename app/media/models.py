from django.db import models
from django.utils import simplejson
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from sorl.thumbnail import get_thumbnail
import markdown
from common.thumbnail.fields import ThumbnailField


IMAGE_FORMATS = {
    'thumbnail': "50x50", 
    'small': "240x180", 
    'medium': "400x250", 
    'large': "615x350"
}

class AttachableImage(models.Model):
    name = models.CharField('Name', max_length=200) # TODO: Make unique for associated object.
    file = ThumbnailField(upload_to='images', blank=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    def clean(self):
        self.name = self.name.lower().replace(' ', '_')
    
    def get_url(self):
        return self.file.url
    url = property(get_url)
    
    def get_thumbnail(self, format, **kwargs):
        size = IMAGE_FORMATS[format]
        return get_thumbnail(self.file, size, **kwargs)


class AttachableModel(models.Model):
    attached_images = generic.GenericRelation(AttachableImage)
    supports_attachments = True
    
    class Meta:
        abstract = True
    
    def get_content_type(self):
        return ContentType.objects.get_for_model(self)
    content_type = property(get_content_type)
    
    def get_rendered_content(self):
        """
        Insert image references and render markdown.
        TODO: Find referenced images and only attach (and generate a thumbnail) when necessary.
        """
        md = markdown.Markdown()
        for image in self.attached_images.all():
            for size in IMAGE_FORMATS.keys():
                thumbnail = image.get_thumbnail(size)
                key = "%s %s" % (image.name, size)
                md.references[key] = (thumbnail.url, '')
            
            md.references['%s %s' % (image.name, 'original')] = (image.url, '')
        
        return md.convert(self.content)
    rendered_content = property(get_rendered_content)

