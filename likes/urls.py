from django.urls import path
from . import views

app_name = 'likes'

urlpatterns = [
    path('likes/', views.product_like, name='product_like'),   
    path('product_like_list/', views.product_like_list, name='product_like_list'), 
]

