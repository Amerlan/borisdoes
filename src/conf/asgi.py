import django
from os import environ
from django.core.asgi import get_asgi_application
from django.core.handlers.asgi import ASGIHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from chats.routing import websocket_urlpatterns


environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
django.setup()
django_app: ASGIHandler = get_asgi_application()


application = ProtocolTypeRouter({
    # "http": django_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
