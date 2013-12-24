from django import forms
from django.db import models
from haystack.forms import ModelSearchForm, model_choices


# Don't show these in the ModelSearchForm.
excluded_models = ()

def filtered_model_choices():
    models = []
    for model_choice in model_choices():
        if not model_choice[0] in excluded_models:
            models.append(model_choice)
    return models


class ExtendedModelSearchForm(ModelSearchForm):
    """
    Extended to exclude models we want to search on, but not show globally.
    """
    def __init__(self, *args, **kwargs):
        super(ExtendedModelSearchForm, self).__init__(*args, **kwargs)
        self.fields['models'] = forms.MultipleChoiceField(
            choices=filtered_model_choices(), 
            required=False, 
            label='Search In', 
            widget=forms.CheckboxSelectMultiple)
    
    def get_model_classes(self, model_list):
        model_classes = []
        for model in model_list:
            model_classes.append(models.get_model(*model.split('.')))
        return model_classes
    
    def get_models(self):
        if self.is_valid() and len(self.cleaned_data['models']):
            models = self.cleaned_data['models']
        else:
            models = [m[0] for m in filtered_model_choices()]
        
        return self.get_model_classes(models)


