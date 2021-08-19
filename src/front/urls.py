from django.urls import path
from .views import LoginPageApi

urlpatterns = [
    path('', LoginPageApi.as_view(),),
]
