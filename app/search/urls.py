from django.conf.urls.defaults import *
from haystack.views import SearchView
from .forms import ExtendedModelSearchForm

urlpatterns = patterns('haystack.views',
    url(r'^$', SearchView(form_class=ExtendedModelSearchForm), name='search'),
)

