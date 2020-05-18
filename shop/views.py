from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    products_liked = Product.objects.filter(users_like=request.user)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html',
                {'category': category,
                'categories': categories,
                'products': products,
                'products_liked': products_liked})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    products_liked = Product.objects.filter(users_like=request.user)
    return render(request, 'shop/product/detail.html',
                            {'product': product,
                            'products_liked': products_liked})  

def base(request):
    return render(request,'shop/base.html')





                          