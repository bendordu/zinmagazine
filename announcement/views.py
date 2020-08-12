from django.shortcuts import render, get_object_or_404, redirect
from .models import Announcement, Comment, Category
from account.models import Profile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from likes.decorators import ajax_required
from chats.models import Chat
from .forms import AnnouncementCreateForm
from uuslug import slugify

def announcement_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    announcements = Announcement.objects.filter(active=True)
    profiles = Profile.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        announcements = Announcement.objects.filter(category=category)
    return render(request, 'announcement_list.html', {'category': category,
                                                    'categories': categories,
                                                    'announcements': announcements,
                                                    'profiles': profiles})

def announcement_detail(request, id, slug):
    announcement = Announcement.objects.get(id=id, slug=slug)
    comments = announcement.comments.filter(active=True) 
    profile = Profile.objects.get(user=announcement.author_ann)
    try:
        chatss = Chat.objects.filter(members=announcement.author_ann.id).filter(members=request.user.id)
    except Chat.DoesNotExist:
        chatss = None
    return render(request, 'announcement_detail.html', {'announcement': announcement,
                                                        'comments': comments,
                                                        'profile': profile,
                                                        'chatss': chatss,})

def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementCreateForm(request.POST)
        if form.is_valid():
            new_ann = form.save(commit=False)
            new_ann.author_ann = request.user
            new_ann.slug = slugify(form.cleaned_data['title'])
            new_ann.save()
            for category in form.cleaned_data['category']:
                new_ann.category.add(category)
            return redirect('announcement:announcement_list')
    else:
        form = AnnouncementCreateForm
    return render(request, 'create_announcement.html', {'form': form})


def edit_announcement(request, id):
    announcement = Announcement.objects.get(id=id)
    if request.method == 'POST':
        form = AnnouncementCreateForm(instance=announcement, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AnnouncementCreateForm(instance=announcement)
    return render(request, 'edit_announcement.html', {'form': form})


@ajax_required
@login_required
@require_POST
def hide_announcement(request):
    announcement = Announcement.objects.get(id=request.POST.get('id'))
    if request.POST.get('action') == 'hide':
        announcement.active = False
    else:
        announcement.active = True
    announcement.save()
    return JsonResponse({'status':'ok'})


def delete_announcement(request, id):
    announcement = Announcement.objects.get(id=id)
    announcement.delete()
    return redirect('dashboard')

@ajax_required
@login_required
@require_POST
def announcement_like(request):
    ann_id = request.POST.get('id')
    action = request.POST.get('action')
    announcement = get_object_or_404(Announcement, id=ann_id)
    if action == 'like':
        announcement.likes.add(request.user)
    else:
        announcement.likes.remove(request.user)
    return JsonResponse({'status':'ok'})

@ajax_required
@login_required
@require_POST
def announcement_add_comment(request):
    ann_id = request.POST.get('id')
    announcement = get_object_or_404(Announcement, id=ann_id)
    if request.POST.get('action'):
        body = request.POST.get('body')
        comment = get_object_or_404(Comment, id=body, author_comment_ann=request.user, announcement=announcement)
        if request.POST.get('action') == 'remove':
            comment.delete()
    else:
        data = request.POST.get('data')
        comment = Comment(body=data, author_comment_ann=request.user, announcement=announcement)
        comment.save()
    return JsonResponse({'status':'ok'})
