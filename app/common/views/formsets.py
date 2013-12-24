from django.views.generic.edit import FormMixin


class FormSetMixin(FormMixin):
    formset_initial = {}
    formset_instance_attributes = {}
    
    def get_formset_initial(self, formset_name):
        """
        Returns the initial data to use for formsets on this view.
        """
        return self.formset_initial
    
    def get_formset_kwargs(self, formset_name):
        """
        Return a dict of kwargs to pass to new formset instances.
        You should return a 'queryset' key with an empty QuerySet on views that 
        create new instances. ex: Model.objects.none()
        """
        kwargs = {'prefix': formset_name } 
        #{'initial': self.get_formset_initial(formset_name)}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs
    
    def get_formset_instance_attributes(self, formset_name):
        """
        Return a dict of attributes to set in specified formset instance before saving.
        """
        return self.formset_instance_attributes
    
    def form_valid(self, form, formsets):
        self.object = form.save()
        for formset_name, formset in formsets.items():
            # Formset saves
            for set_form in formset.forms:
                for k, v in self.get_formset_instance_attributes(formset_name).items():
                    setattr(set_form.instance, k, v)
                try:
                    set_form.save()
                except: # IntegrityError:
                    # Ignore forms which have incomplete data at this point, they
                    # should be empty extra forms.
                    # TODO: Tie into validation or something to verify everything is empty.
                    pass
            
            # Formset deletions
            if hasattr(formset, 'deleted_forms'):
                for set_form in formset.deleted_forms:
                    set_form.instance.delete()
        
        return super(FormSetMixin, self).form_valid(form)
    
    def form_invalid(self, form, formsets):
        return self.render_to_response(self.get_context_data(
            form=form, formsets=formsets))
    
    def get_formsets(self):
        formsets = {}
        for formset_name, formset in self.formsets.items():
            formsets[formset_name] = formset(**self.get_formset_kwargs(formset_name))
        return formsets
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(
            form=self.get_form(self.get_form_class()), 
            formsets=self.get_formsets()))

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        formsets = self.get_formsets()
        
        if form.is_valid() and all([f.is_valid() for k, f in formsets.items()]):
           return self.form_valid(form, formsets)
        else:
            return self.form_invalid(form, formsets)


class FormSetCreateMixin(FormSetMixin):
    def get(self, request, *args, **kwargs):
        self.object = None
        return super(FormSetCreateMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super(FormSetCreateMixin, self).post(request, *args, **kwargs)


class FormSetUpdateMixin(FormSetMixin):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(FormSetUpdateMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(FormSetUpdateMixin, self).post(request, *args, **kwargs)

