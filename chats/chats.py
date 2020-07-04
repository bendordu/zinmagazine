from .models import Chat, Message

class Chats(object):
    def __init__(self, request):
        if request.user.is_active:
            chats = Chat.objects.filter(members=request.user)
        else:
            chats = None 
        self.chats = chats 

    def __len__(self):
        messages = []
        for chat in self.chats:
            messages += Message.objects.filter(chat=chat, is_readed=False)
        return len(messages)


def chats(request):
    return {'chats': Chats(request)}