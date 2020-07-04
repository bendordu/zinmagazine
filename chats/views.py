from django.shortcuts import render, get_object_or_404
from .models import Chat, Message
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from likes.decorators import ajax_required
from django.http import JsonResponse


def chat_list(request):
    chat_list = Chat.objects.filter(members=request.user)
    return render(request, 'chat_list.html', {'chat_list': chat_list})

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
    chat_name = request.POST.get('name')
    chat = Chat.objects.get(name=chat_name)
    if request.POST.get('action'):
        body = request.POST.get('body')
        message = get_object_or_404(Message, id=body, author=request.user, chat=chat)
        if request.POST.get('action') == 'remove':
            message.delete()
    else:
        data = request.POST.get('data')
        message = Message(message=data, author=request.user, chat=chat)
        message.save()
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
