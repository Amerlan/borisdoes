from django.shortcuts import redirect
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status
from chats.serializers import ChatSerializer


class BaseFrontApi(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = (IsAuthenticated,)


class LoginPageApi(BaseFrontApi):
    permission_classes = (AllowAny,)
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('chats/')
        return Response(status=status.HTTP_200_OK)


class RegisterPageApi(BaseFrontApi):
    permission_classes = (AllowAny,)
    template_name = 'signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('chats/')
        return Response(status=status.HTTP_200_OK)


class ChatPageApi(BaseFrontApi):
    template_name = 'chats.html'

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class ChatDetailPageApi(BaseFrontApi):
    template_name = 'detail_chat.html'
    # template_name = 'test.html'

    def get(self, request, chat_id):
        return Response(status=status.HTTP_200_OK, data={'chat_id': chat_id})
