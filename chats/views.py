import os
import shutil
from django.shortcuts import render, get_object_or_404
from .models import Chat, Message
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.dateformat import DateFormat
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings
from likes.decorators import ajax_required
from django.http import JsonResponse
from account.models import Profile


def chat_list(request):
    chat_list = Chat.objects.filter(members=request.user)
    profiles = Profile.objects.all()
    return render(request, 'chat_list.html', {'chat_list': chat_list,
                                              'profiles': profiles})

def chat(request, slug):
    chat = get_object_or_404(Chat, slug=slug)
    messages_text = Message.objects.filter(chat=chat)
    for message in messages_text:
        if message.is_readed == False and message.author != request.user:
            message.is_readed = True
            message.save()
    return render(request, 'chat.html', {'chat': chat,
                                         'messages_text': messages_text})



@ajax_required
@login_required
@require_POST
def message_add(request):
    chat_id = request.POST.get('id')
    chat = Chat.objects.get(id=chat_id)
    data = request.POST.get('data')

    d = {'image0':None, 'image1':None, 'image2':None, 'image3':None, 'image4':None}
    for i in d.keys():
        try:
            d[i] = request.FILES[i]
        except MultiValueDictKeyError:
            continue

    message = Message(message=data, author=request.user, chat=chat, **d)
    message.save()

    if message.image0 or message.image1 or message.image2 or message.image3 or message.image4:
        parent_dir = settings.MEDIA_ROOT 
        try:
            directory = f'messages/{chat.name}'
            path = os.path.join(parent_dir, directory)
            os.makedirs(path)
        except OSError as error:
            pass

        files = ["image0", "image1", "image2", "image3", "image4"]
        for f in files:
            if eval(f"message.{f}"):
                try:
                    message_file = eval(f"message.{f}")
                    initial_path = message_file.path
                    created = DateFormat(message.pub_date).format('d-m-Y-H-i')
                    message_file.name = f'messages/{chat.name}/{chat.name}_message_{message.id}_{message.author}_{created}_{f}.jpg'
                    new_path = os.path.normpath(os.path.join(parent_dir, message_file.name))
                    os.rename(initial_path, new_path) 
                    message.save()
                except OSError:
                    pass
    return JsonResponse({'status':'ok'})
    

@ajax_required
@login_required
@require_POST
def message_remove(request): 
    message_id = request.POST.get('id')
    message = get_object_or_404(Message, id=message_id)
    if request.POST.get('action') == 'remove':
        for image in [message.image0, message.image1, message.image2, message.image3, message.image4]:
            image.delete()
        message.delete()
        if  message.chat.chat.all().count() == 0:
            message.chat.delete()
    if request.POST.get('action') == 'edit':
        text = request.POST.get('body')
        message.body = text
        message.save()
    if request.POST.get('image'):
        image = request.POST.get('image')
        eval(f"message.{image}.delete()")
    return JsonResponse({'status':'ok'})


@ajax_required
@login_required
@require_POST
def new_chat(request):
    chat_name = request.POST.get('name')
    chat = Chat.objects.create(name=chat_name, slug=chat_name)
    member = request.POST.get('member')
    chat.members.add(member)
    chat.members.add(request.user)
    data = request.POST.get('data')
    message = Message.objects.create(message=data, author=request.user, chat=chat)
    return JsonResponse({'status':'ok'})
