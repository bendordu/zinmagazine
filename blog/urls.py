from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('blog/', views.post_list, name='post_list'),
    path('blog/<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('comment/', views.post_add_comment, name='post_add_comment'),
    path('likes/', views.post_like, name='post_like'),  
    path('bookmark_list/', views.bookmark_list, name='bookmark_list'), 
    path('bookmark/', views.bookmark, name='bookmark'), 
]