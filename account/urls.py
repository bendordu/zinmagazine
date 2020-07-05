from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views, profile

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('<int:id>/<slug:slug>/', profile.profile_detail, name='profile_detail'),
    path('profiles/', profile.profile_list, name='profile_list'),
    path('subscribe/', profile.subscribe, name='subscribe'),
    path('news/', profile.news, name='news'),
    
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('<slug:category_slug>/', profile.profile_list, name='profile_list_by_category'),
]