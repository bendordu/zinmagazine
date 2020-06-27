from .models import Post

class Bookmark(object):
    def __init__(self, request):
        if request.user.is_active:
            bookmark = Post.objects.filter(bookmark=request.user)
        else:
            bookmark = None 
        self.bookmark = bookmark 

    def __len__(self):
        return len(self.bookmark)

def bookmark(request):
    return {'bookmark': Bookmark(request)}