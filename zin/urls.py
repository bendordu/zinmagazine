from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orders/', include('orders.urls', namespace='orders')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('likes/', include('likes.urls', namespace='likes')),
    path('chats/', include('chats.urls', namespace='chats')),
    path('account/', include('account.urls')),
    path('proect/', include('proect.urls')),
    path('announcement/', include('announcement.urls', namespace='announcement')),
    path('', include('shop.urls', namespace='shop')),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)