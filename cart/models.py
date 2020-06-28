from django.db import models
from shop.models import Product
from django.conf import settings
from django.core.validators import MinValueValidator
 
class CartUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    get_total_price = models.IntegerField(validators=[MinValueValidator(0)], default=0)
 
    class Meta:
        ordering = ('created',)
 
    def __str__(self):
        return 'CartUser {}'.format(self.id)
 
class CartItem(models.Model):
    cart = models.ForeignKey(CartUser, related_name='cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE, null=True)
    price = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    quantity = models.IntegerField(validators=[MinValueValidator(0)], default=0)
 
    def __str__(self):
        return '{}'.format(self.id)