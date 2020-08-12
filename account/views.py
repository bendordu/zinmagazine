from django.http import HttpResponse
from django.shortcuts import render
from shop.models import Product
from orders.models import Order
from blog.models import Post
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from cart.models import CartUser
from announcement.models import Announcement
from proect.models import Proect


@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    orders = Order.objects.filter(saler=request.user)
    posts = Post.objects.filter(author=request.user)
    products = Product.objects.filter(user=request.user)
    announcements = Announcement.objects.filter(author_ann=request.user)
    subscribe = Profile.objects.filter(subscribers=profile.id)
    proects = Proect.objects.filter(major=profile.id)
    return render(request,'account/dashboard.html', {'profile': profile,
                                                    'orders': orders,
                                                    'posts': posts,
                                                    'products': products,
                                                    'announcements': announcements,
                                                    'subscribe': subscribe,
                                                    'proects': proects})

def delete_profile(request):
    profile = Profile.objects.get(user=request.user)
    profile.delete()
    user = request.user
    user.delete()
    return render(request,'account/delete_profile.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Authenticated successfully')
            else:
                messages.success(request, 'Disabled account')
        else:
            messages.success(request, 'Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user, slug=new_user.username)
            profile.save()
            CartUser.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
        else:
            user_form = UserRegistrationForm()
            messages.error(request, 'Error')
            return render(request,'account/register.html',{'user_form': user_form})
    else:
        user_form = UserRegistrationForm()
        return render(request,'account/register.html',{'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'account/edit.html', {'user_form': user_form,'profile_form': profile_form})