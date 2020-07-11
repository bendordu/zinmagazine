from django.urls import path
from . import views

app_name = 'likes'

urlpatterns = [
    path('likes/', views.product_like, name='product_like'),   
    path('like_list/', views.like_list, name='like_list'), 
]

