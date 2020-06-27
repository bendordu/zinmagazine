from shop.models import Product

class Likes(object):
    def __init__(self, request):
        if request.user.is_active:
            products_liked = Product.objects.filter(users_like=request.user)
        else:
            products_liked = None 
        self.likes = products_liked 

    def __len__(self):
        return len(self.likes)

def likes(request):
    return {'likes': Likes(request)}