from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from likes.decorators import ajax_required
from .models import CategoryMinors, Proect, Minor
from django.utils.text import slugify
from chats.models import Message, Chat
from .forms import ProectCreateForm
from shop.forms import SearchForm
from django.contrib.auth.models import User


def proect_detail(request, id, slug):
    proect = get_object_or_404(Proect, id=id, slug=slug)
    messages_text = Message.objects.filter(chat=proect.chat)
    for message in messages_text:
        if message.is_readed == False and message.author != request.user:
            message.is_readed = True
            message.save()
    search = None
    if request.method == 'POST':
        search = request.POST.get('search')
        user = User.objects.get(username=search)
        minor = Minor.objects.get(user=user) 
    return render(request, 'proect_detail.html', {'proect': proect,
                                                  'messages_text': messages_text,
                                                  'search': search}) 

def create_proect(request):
    if request.method == 'POST':
        form = ProectCreateForm(request.POST)
        if form.is_valid():
            new_proect = form.save(commit=False)
            new_proect.slug = slugify(form.cleaned_data['name'])
            new_proect.major = request.user
            chat = Chat.objects.create(name='proect'+form.cleaned_data['name'], slug='proect'+new_proect.slug)
            chat.members.add(request.user)
            new_proect.chat = chat
            new_proect.save()
        return redirect('dashboard')
    else:
        form = ProectCreateForm
    return render(request, 'create_proect.html', {'form': form})


@ajax_required
@require_POST
def minor_add(request):
    user = User.objects.get(username=request.POST.get('user'))
    minor, created = Minor.objects.get_or_create(user=user) 
    proect_id = request.POST.get('id')
    proect = get_object_or_404(Proect, id=proect_id)
    proect.minors.add(minor.id)
    return JsonResponse({'status':'ok'})

@ajax_required
@require_POST
def minor_search(request):
    search = request.POST.get('search')
    proect_id = request.POST.get('id')
    proect = get_object_or_404(Proect, id=proect_id)
    minorss = proect.minors.all()
    minors = []
    for minor in minorss:
        minors += [minor.user.username]
    try:
        userss = User.objects.filter(username__icontains=search).exclude(username=proect.major).exclude(username__in=minors)
        users = []
        for u in userss:
            users += [u.username]
    except:
        pass
    return JsonResponse({'status':'ok', 'users': users})

    
    