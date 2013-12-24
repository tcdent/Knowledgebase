from django.views.generic import CreateView
from django.http import HttpResponse, HttpResponseServerError
from django.utils import simplejson
from .models import AttachableImage


class AttachableImageCreateView(CreateView):
    model = AttachableImage
    
    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse(simplejson.dumps({
            'name': self.object.name, 
            'thumbnail': self.object.get_thumbnail('thumbnail', crop='center').url
        }))
    
    def form_invalid(self, form):
        return HttpResponseServerError(simplejson.dumps({
            'error': True, 
            'errors': dict(form.errors)
        }))


