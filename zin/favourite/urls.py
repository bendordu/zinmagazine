from django.urls import path
from . import views

app_name = 'favourite'

urlpatterns = [
    path('', views.favourite_detail, name='favourite_detail'),
    path('add/<int:product_id>/', views.favourite_add_remove, name='favourite_add_remove'),
    path('remove/<int:product_id>/', views.cart_remove, name='favourite_remove'),
]