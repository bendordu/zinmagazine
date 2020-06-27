from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Comment
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from likes.decorators import ajax_required


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html',
                {'category': category,
                'categories': categories,
                'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    comments = product.comments.filter(active=True)
    return render(request, 'shop/product/detail.html',
                            {'product': product,
                            'comments': comments}) 

@ajax_required
@login_required
@require_POST
def product_add_comment(request):
    product_id = request.POST.get('id')
    author = request.user
    product = Product.objects.get(id=product_id)
    if request.POST.get('action'):
        body = request.POST.get('body')
        comment = get_object_or_404(Comment, body=body, author=author, product=product)
        if request.POST.get('action') == 'remove':
            comment.delete()
        if request.POST.get('action') == 'edit':
            new_body = request.POST.get('new_body')
            comment.body = new_body
            comment.author = author
            comment.product = product
            comment.save()
    else:
        image = request.POST.get('image')
        data = request.POST.get('data')
        comment = Comment(body=data, author = author, product=product, image=image)
        comment.save()
    return JsonResponse({'status':'ok'})


def base(request):
    return render(request,'shop/base.html')







                          