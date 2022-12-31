from rest_framework.generics import GenericAPIView, ListCreateAPIView
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserPost
from .serializers import UserSerializer, UserListSerializer, MyTokenObtainPairSerializer, OAuth2ObtainPairSerializer, UserPostSerializer
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication, JWTStatelessUserAuthentication
from rest_framework import permissions
from .permissions import IsUserMyself
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView

def username_exists(username):
    return User.objects.filter(username=username).exists()

class RegisterUser(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, format=None):
        allusers = User.objects.all()
        serializer = UserSerializer(allusers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShowUser(GenericAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsUserMyself,)
    serializer_class = UserSerializer

    def get_object(self, pk):
        obj = get_object_or_404(User, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, user_id, format=None):
        user = self.get_object(pk=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id, format=None):
        user = self.get_object(user_id)
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, format=None):
        user = self.get_object(user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BatchUser(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserListSerializer

    def post(self, request, format=None):
        list_serializer = UserListSerializer(data=request.data)
        if list_serializer.is_valid():
            pk_users = User.objects.filter(pk__in=list_serializer.data['uids'])
            pk_serializer = UserSerializer(pk_users, many=True)
            email_users = User.objects.filter(email__in=list_serializer.data['emails'])
            email_serializer = UserSerializer(email_users, many=True)
            return Response({"uids" : pk_serializer.data, "emails": email_serializer.data})
        else:
            return Response(list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPostList(ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserPostSerializer

    def get_queryset(self):
        uid = self.kwargs['user_id']
        return UserPost.objects.filter(user=uid)

    def perform_create(self, serializer):
        uid = self.kwargs['user_id']
        user = User.objects.get(pk=uid)
        userpost = serializer.save(user=user)
        return userpost

class CustomAuthToken(ObtainAuthToken):
    # authentication_classes is default defined in setting.py
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = MyTokenObtainPairSerializer
    

class MyOAuth2TokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = OAuth2ObtainPairSerializer

    def post(self, request, *args, **kwards):
        # id_token = request.headers.get('id_token')
        # google_validate_id_token(id_token=id_token)
        serializer = OAuth2ObtainPairSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    