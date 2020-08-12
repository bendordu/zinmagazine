from django import forms
from .models import Product, Category

class ProductCreateForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Product
        fields = ('name', 'category', 'year', 'author_product', 'publisher', 
                  'description', 'price', 'available', 'quantity_pr', 'type_pr', 
                  'price_type', 'image', 'image_dop1', 'image_dop2', 'file_product')

class SearchForm(forms.Form):
    search = forms.CharField()