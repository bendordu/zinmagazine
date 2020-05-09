from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from shop.models import Product
from .favourite import Favourite
from .forms import FavouriteAddProductForm


@require_POST
def favourite_add_remove(request, product_id):
    favourite = Favourite(request)
    product = get_object_or_404(Product, id=product_id)
    form = FavouriteAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        favourite.add(product=product, add_favourite=cd['add_favourite'])
    return redirect(request.META.get('HTTP_REFERER'))

def cart_remove(request, product_id):
    favourite = Favourite(request)
    product = get_object_or_404(Product, id=product_id)
    favourite.remove(product)
    return redirect('favourite:favourite_detail')

def favourite_detail(request):
    favourite = Favourite(request)
    return render(request, 'detail.html', {'favourite': favourite})
