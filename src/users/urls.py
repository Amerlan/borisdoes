from django.urls import path
from .views import LoginApi, LogoutApi, RegisterApi

urlpatterns = [
    path('login/', LoginApi.as_view()),
]
