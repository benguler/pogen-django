from django import forms
from params.models import Params

class ParamsForm(forms.ModelForm):
    class Meta:
        model   = Params
        fields  = ['genre', 'syls']