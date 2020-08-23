from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.bas, name='bas'),
    path('shop/', views.product_list, name='product_list'),
    path('comment/', views.product_add_comment, name='product_add_comment'),
    path('product_remove_comment/', views.product_remove_comment, name='product_remove_comment'),
    path('product_s/', views.product_s, name='product_s'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product_bye_paper/', views.product_bye_paper, name='product_bye_paper'),
    path('create_product/', views.create_product, name='create_product'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('hide_product/', views.hide_product, name='hide_product'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('product_comment_like/', views.product_comment_like, name='product_comment_like'),
    path('type_pr/<slug:type_pr_slug>/', views.product_list, name='product_list_by_type_pr'),
    path('price_type/<slug:price_type_slug>/', views.product_list, name='product_list_by_price_type'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
]