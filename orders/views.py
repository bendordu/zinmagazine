from django.shortcuts import render
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from cart.context_processors import CartOfUser
from shop.models import Product
from cart.models import CartUser, CartItem

def order_create(request):
    if request.user.is_active:
        cart = CartOfUser(request)
    else:
        cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            if request.user.is_active:
                order.saler = request.user
                order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
                p = Product.objects.get(name=item['product'])
                p.quantity_pr = item['quantity_pr']
                p.count_order += item['quantity']
                p.save()
                if request.user.is_active:
                    c = CartUser.objects.get(user=request.user)
                    i = CartItem.objects.get(cart=c, product=p)
                    i.delete()
                    c.get_total_price = 0
                    c.save()
            if not request.user.is_active:
                cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


def order_list(request):
    orders = Order.objects.filter(saler=request.user)
    items = OrderItem.objects.filter(order__in=orders)
    return render(request, 'orders/order/order_detail.html', {'orders': orders, 'items': items})

    