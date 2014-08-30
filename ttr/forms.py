from django.forms import ModelForm, ValidationError
from django.forms.models import modelform_factory
from .models import *

class InfractionForm(ModelForm):
    class Meta:
        model = Infraction

    def clean(self):
        cleaned_data = super(InfractionForm, self).clean()

        if cleaned_data.get('change_level', False) is False and not cleaned_data.get('speedchat_only', False) and not cleaned_data.get('no_true_friends', False) and not cleaned_data.get('no_community_areas', False):
            raise ValidationError("You need to specify at least one consequence!", code='required')

        return cleaned_data

InfractionSubjectForm = modelform_factory(InfractionSubject)