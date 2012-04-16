import simplejson
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, ListView as DjangoListView, DetailView as DjangoDetailView
from django.views.generic.detail import SingleObjectMixin


class ContextMixin(View):
    def get_context_data(self, **kwargs):
        context = super(ContextMixin, self).get_context_data(**kwargs)
        if self.model:
            context['app_name'] = unicode(self.model._meta.app_label)
        return context

class AuthenticatedView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AuthenticatedView, self).dispatch(request, *args, **kwargs)


class ListView(ContextMixin, DjangoListView):
    pass


class DetailView(ContextMixin, DjangoDetailView):
    pass


class RatingView(SingleObjectMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RatingView, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.rating.add(
            score=request.POST['score'], 
            user=request.user, 
            ip_address=request.META['REMOTE_ADDR'])

        return HttpResponse(simplejson.dumps(dict(success=True)), mimetype='application/json')

