from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import GroupSerializer, UserSerializer, LogInSerializer
from .permissions import IsGroupAdmin

User = get_user_model()

class SignUpView(generics.CreateAPIView):
    """
    API Endpoint for admin to add users
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser, ]


class LogInView(TokenObtainPairView):
    """
    Login Endpoint for users
    Access and Refresh tokens are returned
    """
    serializer_class = LogInSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for groups
    Only Users who creeated the group can modify or delete it
    Chat room URL is included in the response
    """
    serializer_class = GroupSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated, IsGroupAdmin]

    def get_queryset(self):
        """
        Returns all groups which current user is enlisted in
        """
        return self.request.user.members.prefetch_related('members')

    def filter_queryset(self, queryset):
        """
        Filters the queryset if search parameters are passed
        in request
        """
        if self.request.query_params and not self.kwargs.get('slug'):
            search = self.request.query_params.get('search')
            queryset =queryset.filter(slug__contains = search)
        return queryset
    
    
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API Endpoint for Users
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]

    def filter_queryset(self, queryset):
        """
        Filters the queryset if search parameters are passed
        in request
        """
        if self.request.query_params and not self.kwargs.get('id'):
            search = self.request.query_params.get('search')
            queryset =queryset.filter(username__contains = search)
        return queryset


@login_required
def room(request,room_name):
    """
    View to render the Chat page
    """
    user = request.user
    groups = user.members.values_list('slug', flat = True)
    if not room_name in groups:
        raise Http404
    groups = list(groups)
    groups.remove(room_name)
    return render(request, 'chat/room.html', {
        'room_name' : room_name,
        'username' : user.username,
        'groups': groups,
        'user': user
    })