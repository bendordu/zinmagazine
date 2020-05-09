from .favourite import Favourite

def favourite(request):
    return {'favourite': Favourite(request)}