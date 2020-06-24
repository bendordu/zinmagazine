from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from shop.models import Product
from .cart import Cart
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from likes.decorators import ajax_required


@ajax_required
#@login_required
@require_POST
def cart_add_product(request):
    cart = Cart(request)
    product_id = request.POST.get('id')
    action = request.POST.get('action')
    product = Product.objects.get(id=product_id)
    if action == 'minus':
        cart.minus(product=product)
    elif action == 'remove':
        cart.remove(product=product)
    else:
        cart.add(product=product)
    return JsonResponse({'status':'ok'})

def cart_detail(request):
    cart = Cart(request)
    if request.user.is_active:
        products_liked = Product.objects.filter(users_like=request.user)
    else:
        products_liked = None
    return render(request, 'cart/detail.html', {'cart': cart, 'products_liked': products_liked})




