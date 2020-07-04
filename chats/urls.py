from django.urls import path
from . import views

app_name = 'chats'

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('<slug:slug>/', views.chat, name='chat'),
    path('new_chat', views.new_chat, name='new_chat'),
    path('message_add', views.message_add, name='message_add'),
]