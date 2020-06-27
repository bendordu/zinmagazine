from django.db import models
from shop.models import Product
from django.conf import settings

class CartUser(models.Model):
    product = models.ManyToManyField(Product, related_name='product', blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE) 
    count_product = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return '{} {}'.format(self.user.name, self.created)