from django import forms

class FavouriteAddProductForm(forms.Form):
    add_favourite = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)