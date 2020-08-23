from .models import Chat, Message

class Chats(object):
    def __init__(self, request):
        if request.user.is_active:
            chats = Chat.objects.filter(members=request.user)
            messages = 0
            for chat in chats:
                messages += Message.objects.filter(chat=chat, is_readed=False).exclude(author=request.user).count()
        else:
            chats = None 
            messages = None
        self.messages = messages

    def __len__(self):
        return self.messages


def chats(request):
    return {'chats': Chats(request)}