from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('order_list/', views.order_list, name='order_list'),
]