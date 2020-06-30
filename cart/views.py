from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from shop.models import Product
from .cart import Cart
from .models import CartUser, CartItem
from django.http import JsonResponse, HttpResponse
from likes.decorators import ajax_required
from .context_processors import CartOfUser


@ajax_required
@require_POST
def cart_add_product(request):
    product_id = request.POST.get('id')
    action = request.POST.get('action')
    product = Product.objects.get(id=product_id)
    if action == 'minus':
        if request.user.is_active:
            cart = CartUser.objects.get(user=request.user)
            item = CartItem.objects.get(cart=cart, product=product)
            if item.quantity == 1:
                item.delete()
            else:
                item.price -= product.price
                item.quantity -= 1
                item.save()
            cart.get_total_price -= product.price 
            cart.save()
        else:
            cart = Cart(request)
            cart.minus(product=product)
    elif action == 'remove':
        if request.user.is_active:
            cart = CartUser.objects.get(user=request.user)
            item = CartItem.objects.get(cart=cart, product=product)
            item.delete()
            cart.get_total_price -= product.price * item.quantity
            cart.save()
        else:
            cart = Cart(request)
            cart.remove(product=product)
    else:
        if request.user.is_active:
            cart = CartUser.objects.get(user=request.user)
            try:
                item = CartItem.objects.get(cart=cart, product=product)
                item.price += product.price
                item.quantity += 1
                item.save()
            except: 
                CartItem.objects.create(cart=cart, product=product, price=product.price, quantity=1)
            finally:
                cart.get_total_price += product.price 
                cart.save()
        else:
            cart = Cart(request)
            cart.add(product=product)
    return JsonResponse({'status':'ok'})

def cart_detail(request):
    if request.user.is_active:
        cart_user = CartOfUser(request)
        return render(request, 'cart/detail_user.html', {'cart_user': cart_user})
    else:
        cart = Cart(request)
        return render(request, 'cart/detail.html', {'cart': cart})




