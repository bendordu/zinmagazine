from django import forms
from .models import Product, Category

class ProductCreateForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Product
        fields = ('name', 'category', 'description', 'price', 'available', 'quantity_pr', 'type_pr', 'price_type')

class SearchForm(forms.Form):
    search = forms.CharField()