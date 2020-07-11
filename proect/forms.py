from django import forms
from .models import Proect

class ProectCreateForm(forms.ModelForm):
    class Meta:
        model = Proect
        fields = ('name', 'description', 'active')