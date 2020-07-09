from django import forms
from .models import Announcement, Category

class AnnouncementCreateForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Announcement
        fields = ('title', 'category', 'body', 'active')