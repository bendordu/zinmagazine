from django.urls import path
from . import views

app_name = 'announcement'

urlpatterns = [
    path('announcement/', views.announcement_list, name='announcement_list'),
    path('announcement_like/', views.announcement_like, name='announcement_like'),
    path('announcement_add_comment/', views.announcement_add_comment, name='announcement_add_comment'),
    path('create_announcement/', views.create_announcement, name='create_announcement'),
    path('<slug:category_slug>/', views.announcement_list, name='announcement_list_by_category'),
    path('<int:id>/<slug:slug>/', views.announcement_detail, name='announcement_detail'),
    
]