from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import GroupViewSet, LogInView, SignUpView, UserViewSet,room

app_name = 'chat'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LogInView.as_view(), name='login'),
    path('token-refresh/',TokenRefreshView.as_view(), name= 'refresh_token'),
    path('chat/<str:room_name>/',room, name= 'chat'),
]

router = SimpleRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'users', UserViewSet, basename='users')

urlpatterns += router.urls