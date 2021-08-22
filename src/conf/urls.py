from django.contrib import admin
from django.urls import path, include

api_urlpatterns = [
    path('users/', include('users.urls')),
    path('chats/', include('chats.urls')),
]


urlpatterns = [
    path('', include('front.urls')),
    path('api/', include(api_urlpatterns)),
        # path('admin/', admin.site.urls),
]
