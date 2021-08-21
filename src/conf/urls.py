from django.contrib import admin
from django.urls import path, include

api_urlpatterns = [
    path('users/', include('users.urls'))
]


urlpatterns = [
    path('', include('front.urls')),
    path('api/', include(api_urlpatterns)),
        # path('admin/', admin.site.urls),
]
