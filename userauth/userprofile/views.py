from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserListSerializer
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

def username_exists(username):
    return User.objects.filter(username=username).exists()

class RegisterUser(APIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny,)

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

class ShowUser(APIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, user_id, format=None):
        user = get_object_or_404(User, pk=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id, format=None):
        user = get_object_or_404(User, pk=user_id)
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BatchUser(APIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny,)

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


class CustomAuthToken(ObtainAuthToken):

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


    