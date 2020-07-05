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
    return render(request, 'blog/blog.html', {'posts': posts})
    

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',publish__year=year,publish__month=month,publish__day=day)
    comments = post.comments.filter(active=True) 
    return render(request,'blog/post/detail.html',{'post': post,
                                                    'comments': comments})

def bookmark_list(request):
    if request.user.is_active:
        bookmark_list = Post.objects.filter(bookmark=request.user)
    else:
        bookmark_list = None
    return render(request, 'blog/bookmark_list.html', {'bookmark_list': bookmark_list})

@ajax_required
@login_required
@require_POST
def post_add_comment(request):
    title = request.POST.get('title')
    data = request.POST.get('data')
    post = get_object_or_404(Post, title=title)
    author = request.user
    if request.POST.get('action'):
        body = request.POST.get('body')
        comment = get_object_or_404(Comment, body=body, author_comment=author, post=post)
        if request.POST.get('action') == 'remove':
            comment.delete()
        if request.POST.get('action') == 'edit':
            new_body = request.POST.get('new_body')
            comment.body = new_body
            comment.author = author
            comment.product = product
            comment.save()
    else:
        data = request.POST.get('data')
        comment = Comment(body=data, author_comment=author, post=post)
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

@ajax_required
@login_required
@require_POST
def bookmark(request):
    title = request.POST.get('title')
    action = request.POST.get('action')
    post = get_object_or_404(Post, title=title)
    if action == 'bookmark':
        post.bookmark.add(request.user)
    else:
        post.bookmark.remove(request.user)
    return JsonResponse({'status':'ok'})