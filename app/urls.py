from django import http
from django.conf import settings
from django.conf.urls.defaults import *
from django.template import Context, RequestContext, loader
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.decorators.csrf import requires_csrf_token
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    #(r'^search/', include('app.search.urls')), 
    
    url(r'^', include('app.media.urls', namespace='media')), 
    url(r'^', include('app.pages.urls', namespace='pages')), 
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()


@requires_csrf_token
def page_not_found(request):
    t = loader.get_template('404.html')
    return http.HttpResponseNotFound(t.render(RequestContext(request, {'request_path': request.path})))

handler404 = page_not_found


@requires_csrf_token
def server_error(request):
    t = loader.get_template('500.html')
    return http.HttpResponseServerError(t.render(RequestContext(request, {'request_path': request.path})))

handler500 = server_error

