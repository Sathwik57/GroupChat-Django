"""
ASGI config for testchat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from chat.middleware import TokenAuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chat import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testchat.settings.local')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": 
        TokenAuthMiddlewareStack(
            URLRouter(routing.websocket_urlpatterns)
        ),
    }
)
