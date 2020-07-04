from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.base, name='base'),
    path('shop/', views.product_list, name='product_list'),
    path('comment/', views.product_add_comment, name='product_add_comment'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product_bye_paper/', views.product_bye_paper, name='product_bye_paper'),
    path('type_pr/<slug:type_pr_slug>/', views.product_list, name='product_list_by_type_pr'),
    path('price_type/<slug:price_type_slug>/', views.product_list, name='product_list_by_price_type'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
]