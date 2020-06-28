from django.contrib import admin
from .models import CartUser, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']

@admin.register(CartUser)
class CartUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created']
    inlines = [CartItemInline]