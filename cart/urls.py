from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('cart_add_product/', views.cart_add_product, name='cart_add_product'),      
]