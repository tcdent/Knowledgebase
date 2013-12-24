from datetime import datetime
from django import forms
from django.db import models
from django.utils.http import urlencode, urlquote
import reversion
from media.models import AttachableModel


class Page(AttachableModel):
    parent = models.ForeignKey('self', blank=True, null=True)
    title = models.CharField('Title', max_length=200)
    content = models.TextField('Content', blank=True, null=True)
    created = models.DateTimeField('Creation Date', auto_now_add=True)
    updated = models.DateTimeField('Update Date', auto_now=True)
    
    class Meta:
        unique_together = ('parent', 'title')
    
    def __unicode__(self):
        return self.title
    
    def get_slug(self):
        slug = urlquote(self.title.replace(' ', '_'))
        if not self.parent:
            return slug
        return "/".join([self.parent.slug, slug])
    slug = property(get_slug)
    
    def get_parents(self):
        parents = []
        parent = self.parent
        while parent:
            page = Page.objects.get(pk=parent.pk)
            parent = page.parent
            parents.append(page)
        return list(reversed(parents))
    parents = property(get_parents)
    
    def get_children(self):
        return Page.objects.filter(parent__pk=self.pk)
    children = property(get_children)
    
    def get_revisions(self):
        return reversion.get_for_object(self)
    
    def get_unique_revisions(self):
        return reversion.get_unique_for_object(self)
    revisions = property(get_unique_revisions)
    
    @models.permalink
    def get_absolute_url(self):
        return ('pages:view', [], {'slug': self.slug })


class PageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        
        # Insert each page into the appropriate position in a list of parent-less 
        # pages and indent for clarity.
        
        def get_indented_children(parent, level=1):
            children = []
            for child in parent.children:
                if child.pk == self.instance.pk:
                    continue # Don't allow nesting a page under itself. 
                
                child.title = "%s %s" % (("-" * level), child.title)
                children.append(child)
                [children.append(c) for c in get_indented_children(child, level + 1)]
            return children
        
        parents = Page.objects.filter(parent=None)
        if self.instance:
            parents.exclude(pk=self.instance.pk)
        
        parent_list = []
        for parent in parents:
            parent_list.append(parent)
            parent_list.extend(get_indented_children(parent))
        
        field = self.fields['parent']
        choices = [(field.prepare_value(obj), field.label_from_instance(obj)) for obj in parent_list]
        choices.insert(0, ('', "Root"))
        self.fields['parent'].choices = choices
    
    class Meta:
        model = Page


