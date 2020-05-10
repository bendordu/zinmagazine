from django.conf import settings
from shop.models import Product

class Favourite(object):
    def __init__(self, request):
        self.session = request.session
        favourite = self.session.get(settings.FAVOURITE_SESSION_ID)
        if not favourite:
            favourite = self.session[settings.FAVOURITE_SESSION_ID] = {}
        self.favourite = favourite
    
    def add(self, product, add_favourite=False):
        product_id = str(product.id)
        if product_id not in self.favourite:
            self.favourite[product_id] = {'count': 0}
        if self.favourite[product_id]['count'] < 1:
            self.favourite[product_id]['count'] += 1
        else: 
            del self.favourite[product_id]
            self.save()    
        self.save()

    def save(self):
        self.session.modified = True 

    def __iter__(self):
        product_ids = self.favourite.keys()
        products = Product.objects.filter(id__in=product_ids)

        favourite = self.favourite.copy()
        for product in products:
            favourite[str(product.id)]['product'] = product

        for item in favourite.values():
            item['count'] = int(item['count'])
            yield item   

    def color(self):
        product_ids = self.favourite.keys()
        products = Product.objects.filter(id__in=product_ids)

        return products

    def __len__(self):
        return sum(item['count'] for item in self.favourite.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()