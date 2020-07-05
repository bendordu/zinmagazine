from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from likes.decorators import ajax_required
from .models import Profile, CategoryProfile
from chats.models import Chat
from orders.models import Order
from blog.models import Post
from shop.models import Product
from announcement.models import Announcement
from itertools import chain
from operator import attrgetter


def profile_detail(request, id, slug):
    profile = get_object_or_404(Profile, id=id, slug=slug)
    orders = Order.objects.filter(saler=profile.user)
    posts = Post.objects.filter(author=profile.user)
    products = Product.objects.filter(user=profile.user)
    announcements = Announcement.objects.filter(author_ann=profile.user)
    try:
        chatss = Chat.objects.filter(members=profile.user.id).filter(members=request.user.id)
    except Chat.DoesNotExist:
        chatss = None
    return render(request,'profile/profile_detail.html', {'profile': profile,
                                                          'orders': orders,
                                                          'posts': posts,
                                                          'products': products,
                                                          'chatss': chatss,
                                                          'announcements': announcements})

def profile_list(request, category_slug=None):
    category = None
    categories = CategoryProfile.objects.all()
    profiles = Profile.objects.all()
    if category_slug:
        category = get_object_or_404(CategoryProfile, slug=category_slug)
        profiles = Profile.objects.filter(category=category)
    return render(request,'profile/profile_list.html', {'category': category,
                                                        'categories': categories,
                                                        'profiles': profiles})
def news(request):
    profiles = Profile.objects.filter(subscribers=request.user)
    isubscribe = []
    for profile in profiles:
        isubscribe += str(profile.user.id)
    posts = Post.objects.filter(author__in=isubscribe)
    products = Product.objects.filter(user__in=isubscribe)
    announcements = Announcement.objects.filter(author_ann__in=isubscribe)
    news = sorted(chain(posts, products, announcements), key=attrgetter('created'), reverse = True)
    return render(request,'profile/news.html', {'posts': posts,
                                                'products': products,
                                                'announcements': announcements,
                                                'news': news,
                                                'profiles': profiles})

@ajax_required
@login_required
@require_POST
def subscribe(request):
    profile_id = request.POST.get('id')
    action = request.POST.get('action')
    profile = Profile.objects.get(id=profile_id)
    if action == 'subscribe':
        profile.subscribers.add(request.user)
    else:
        profile.subscribers.remove(request.user)
    return JsonResponse({'status':'ok'})

    
