from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.base, name='base'),
    path('shop/', views.product_list, name='product_list'),
    path('comment/', views.product_add_comment, name='product_add_comment'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]