from django.urls import path
from . import views

app_name = 'proect'

urlpatterns = [
    path('<int:id>/<slug:slug>/', views.proect_detail, name='proect_detail'),
    path('create_proect/', views.create_proect, name='create_proect'),
    path('minor_add/', views.minor_add, name='minor_add'),
]