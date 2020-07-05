from .models import Profile

class ISubscribe(object):
    def __init__(self, request):
        if request.user.is_active:
            isubscribe = Profile.objects.filter(subscribers=request.user)
        else:
            isubscribe = None 
        self.isubscribe = isubscribe

    def __len__(self):
        return len(self.isubscribe)

def isubscribe(request):
    return {'isubscribe': ISubscribe(request)}
