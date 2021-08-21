from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status


class LoginPageApi(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class RegisterPageApi(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'signup.html'

    def get(self, request):
        return Response(status=status.HTTP_200_OK)
