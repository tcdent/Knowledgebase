from django.conf.urls.defaults import *
from .views import AttachableImageCreateView

urlpatterns = patterns('media.views',
    url(r'^attach_image', AttachableImageCreateView.as_view(), name='attach_image'), 
)

