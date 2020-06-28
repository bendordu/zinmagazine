from .cart import Cart
from .models import CartItem, CartUser
from shop.models import Product

def cart(request):
    return {'cart': Cart(request)}


class CartOfUser(object):
    def __init__(self, request):
        self.cart_user = CartUser.objects.get(user=request.user)
         
    def __len__(self):
        quantity_items = 0
        try:
            items = CartItem.objects.filter(cart=self.cart_user)
            for item in items:
                quantity_items += item.quantity
        except ObjectDoesNotExist: 
            quantity_items = 0
        return quantity_items

    def __iter__(self):
        items = CartItem.objects.filter(cart=self.cart_user)
        cart_user = {} 

        for item in items:
            cart_user[str(item.product.id)] = {'quantity': item.quantity}

        products = Product.objects.filter(id__in=cart_user.keys())

        for product in products:
            cart_user[str(product.id)].update({'product': product, 'price': str(product.price), 'quantity_pr': int(product.quantity_pr)})

        for item in cart_user.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['quantity_pr'] -= item['quantity']
            yield item
        
    def get_total_price(self):
        return self.cart_user.get_total_price

    def products(self):
        items = CartItem.objects.filter(cart=self.cart_user)
        products = []
        for item in items:
            products += str(item.product.id)
        product = Product.objects.filter(id__in=products)
        return product
       

def cart_user(request):
    if request.user.is_active:
        cart_user = CartOfUser(request)
    else:
        cart_user = None
    return {'cart_user': cart_user}