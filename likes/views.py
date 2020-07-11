from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .decorators import ajax_required
from shop.models import Product
from blog.models import Post
from announcement.models import Announcement
from account.models import Profile

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

def like_list(request):
    if request.user.is_active:
        products_liked = Product.objects.filter(users_like=request.user)
        post_liked = Post.objects.filter(users_like=request.user)
        ann_liked = Announcement.objects.filter(likes=request.user)
        profiles = Profile.objects.all()
    else:
        products_liked = None
        post_liked = None
        ann_liked = None
        profiles = None
    return render(request, 'like_list.html', {'products_liked': products_liked,
                                              'post_liked': post_liked,
                                              'ann_liked': ann_liked,
                                              'profiles': profiles})