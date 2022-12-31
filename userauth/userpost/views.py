from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth.models import User
from .models import UserPost
from .serializers import UserPostSerializer
from rest_framework import permissions
from userprofile.permissions import IsOwnerOrReadOnly
from rest_framework import parsers

# Create your views here.

class UserPostList(ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = UserPostSerializer

    def get_queryset(self):
        uid = self.kwargs['user_id']
        return UserPost.objects.filter(user=uid)

class UserPostAdd(CreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = UserPostSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def perform_create(self, serializer):
        uid = self.request.user.id
        user = User.objects.get(pk=uid)
        userpost = serializer.save(user=user)
        return userpost

class UserPostDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly, ]
    queryset = UserPost.objects.all()
    serializer_class = UserPostSerializer