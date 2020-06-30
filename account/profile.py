from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Profile, CategoryProfile


def profile_detail(request, id, slug):
    profile = get_object_or_404(Profile, id=id, slug=slug)
    return render(request,'profile/profile_detail.html', {'profile': profile})

def profile_list(request, category_slug=None):
    category = None
    categories = CategoryProfile.objects.all()
    profiles = Profile.objects.all()
    if category_slug:
        category = get_object_or_404(CategoryProfile, slug=category_slug)
        profiles = Profile.objects.filter(category=category)
    return render(request,'profile/profile_list.html', {'category': category,
                                                        'categories': categories,
                                                        'profiles': profiles})

    
