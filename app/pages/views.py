from string import capwords
from django.views.generic import View, TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin
from django.http import Http404
from django.contrib import messages
from reversion.helpers import generate_patch_html
from .models import Page, PageForm


class PageFormMixin(ModelFormMixin):
    form_class = PageForm
    template_name = "pages/edit.html"
    
    def get_initial(self):
        initial = dict()
        if self.request.GET.get('parent_id'):
            initial['parent'] = self.request.GET.get('parent_id')
        return initial
    
    def get_success_message(self):
        return "%s '%s' was succesfully %sd." % (
            capwords(self.object._meta.verbose_name), 
            unicode(self.object), 
            self.action_name
        )
    
    def form_valid(self, form):
        result = super(PageFormMixin, self).form_valid(form)
        messages.success(self.request, self.get_success_message())
        return result


class ExistingObjectView(View):
    def get_object(self, queryset=None):
        try:
            # Separate out URL sections and pop the furthest token. 
            # Repeat until we have a unique matching entry.
            cycle = 1
            slugs = self.kwargs['slug'].replace('_', ' ').split('/')
            queryset = Page.objects.filter(title=slugs.pop())
            while len(queryset) > 1:
                conditions = {}
                conditions["%stitle" % ("parent__" * cycle)] = slugs.pop()
                queryset = queryset.filter(**conditions)
                cycle += 1
            return queryset[0]
        except Exception:
            raise Http404()


class PageView(ExistingObjectView, DetailView):
    model = Page
    template_name = "pages/base.html"


class PageDiffView(PageView):
    template_name = "pages/diff.html"
    
    def get_context_data(self, **kwargs):
        context = super(PageDiffView, self).get_context_data(**kwargs)
        page = self.get_object()
        revisions = page.get_unique_revisions()
        selected_revision = page.get_revisions().get(pk=self.kwargs['revision'])
        context['page'] = page
        context['revision'] = selected_revision
        context['title'] = generate_patch_html(selected_revision, revisions[0], 'title', cleanup='semantic')
        context['content'] = generate_patch_html(selected_revision, revisions[0], 'content', cleanup='semantic')
        return context


class PageCreateView(PageFormMixin, CreateView):
    model = Page
    action_name = "create"


class PageUpdateView(PageFormMixin, ExistingObjectView, UpdateView):
    model = Page
    action_name = "update"


class PageDeleteView(PageFormMixin, ExistingObjectView, DeleteView):
    model = Page
    action_name = "delete"
    success_url = "/"
    
    def get(self, *args, **kwargs):
        response = self.delete(*args, **kwargs)
        messages.success(self.request, self.get_success_message())
        return response


class IndexView(TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['pages'] = Page.objects.filter(parent=None)
        return context


