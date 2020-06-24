from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from shop.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from likes.decorators import ajax_required

def post_list(request):
    posts = Post.published.all()
    if request.user.is_active:
        products_liked = Product.objects.filter(users_like=request.user)
    else:
        products_liked = None
    return render(request, 'blog/blog.html', {'posts': posts,
                                            'products_liked': products_liked})
    

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',publish__year=year,publish__month=month,publish__day=day)
    comments = post.comments.filter(active=True)
    author = (request.user)   
    if request.user.is_active:
        products_liked = Product.objects.filter(users_like=request.user)
    else:
        products_liked = None 
    return render(request,'blog/post/detail.html',{'post': post,
                                                    'comments': comments,
                                                    'products_liked': products_liked})

@ajax_required
@login_required
@require_POST
def post_add_comment(request):
    title = request.POST.get('title')
    data = request.POST.get('data')
    post = get_object_or_404(Post, title=title)
    author = request.user
    comment = Comment(body=data[5:], author_comment = author, post=post)
    comment.save()
    return JsonResponse({'status':'ok'})

@ajax_required
@login_required
@require_POST
def post_like(request):
    title = request.POST.get('title')
    action = request.POST.get('action')
    post = get_object_or_404(Post, title=title)
    if action == 'like':
        post.users_like.add(request.user)
    else:
        post.users_like.remove(request.user)
    return JsonResponse({'status':'ok'})