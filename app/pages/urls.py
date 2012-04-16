from django.conf.urls.defaults import *
from .views import IndexView, PageView, PageDiffView, PageCreateView, PageUpdateView, PageDeleteView

urlpatterns = patterns('pages.views',
    url(r'^$', IndexView.as_view(), name='home'), 
    url(r'^create/$', PageCreateView.as_view(), name='create'), 
    url(r'^(?P<slug>.*)/diff/(?P<revision>.*)/$', PageDiffView.as_view(), name='diff'), 
    url(r'^(?P<slug>.*)/edit/$', PageUpdateView.as_view(), name='edit'), 
    url(r'^(?P<slug>.*)/delete/$', PageDeleteView.as_view(), name='delete'),
    url(r'^(?P<slug>.*)/$', PageView.as_view(), name='view'), 
)

