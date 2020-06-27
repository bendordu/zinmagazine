from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .decorators import ajax_required
from shop.models import Product

@ajax_required
@login_required
@require_POST
def product_like(request):
    product_id = request.POST.get('id')
    action = request.POST.get('action')
    product = Product.objects.get(id=product_id)
    if action == 'like':
        product.users_like.add(request.user)
    else:
        product.users_like.remove(request.user)
    return JsonResponse({'status':'ok'})

def product_like_list(request):
    if request.user.is_active:
        products_liked = Product.objects.filter(users_like=request.user)
    else:
        products_liked = None
    return render(request, 'product_like_list.html', {'products_liked': products_liked})