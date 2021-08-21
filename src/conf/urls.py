from django.contrib import admin
from django.urls import path, include

api_urlpatterns = [
    path('', include('users.urls'))
]

front_urlpattenrs = [
    path('login/', include('front.urls')),
]

urlpatterns = [
    path('', include(front_urlpattenrs)),
    path('api/', include(api_urlpatterns)),
        # path('admin/', admin.site.urls),
]
