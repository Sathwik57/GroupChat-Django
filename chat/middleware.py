from urllib.parse import parse_qs
from channels.auth import AuthMiddleware,AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.sessions import CookieMiddleware,SessionMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken


User = get_user_model()

@database_sync_to_async
def get_user(scope):
    """
    Middleware function to add user to scope
    of the ws connection
    """
    query_string = parse_qs(scope['query_string'].decode())
    token = query_string.get('token')
    if not token:
        return AnonymousUser()
    try:
        access_token = AccessToken(token[0])
        user = User.objects.get(id = access_token['id'])
    except Exception as e:
        return AnonymousUser()
    if not user.is_active:
        return AnonymousUser()
    return user


class TokenAuthMiddleware(AuthMiddleware):
    async def resolve_scope(self, scope):
        return await super().resolve_scope(scope)


def TokenAuthMiddlewareStack(inner):
    return CookieMiddleware(SessionMiddleware(TokenAuthMiddleware(inner)))














