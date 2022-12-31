from rest_framework import serializers
from .models import Profile, UserPost, PostImage
from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import update_last_login

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('id', 'user', 'create_date')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'profile')
        read_only_fields = ('id', )

    def validate_email(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Email Already Exist")
        return value

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')

        user = User.objects.create_user(username=validated_data['email'],
                                    email=validated_data['email'],
                                    password=validated_data['password'],
                                    first_name=validated_data.get('first_name', ''),
                                    last_name=validated_data.get('last_name', ''))
        Profile.objects.create(user=user, **profile_data)
        return user


    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()

        profile.name = profile_data.get('name', profile.name)
        profile.phone = profile_data.get('phone', profile.phone)
        profile.iconid = profile_data.get('iconid', profile.iconid)
        profile.description = profile_data.get('description', profile.description)
        profile.save()

        return instance

class UserListSerializer(serializers.Serializer):     
    uids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    emails = serializers.ListField(
        child=serializers.EmailField(),
        required=False
    )

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["id", "userpost", "image"]

class UserPostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length=10000, allow_empty_file=False, use_url=False),
        write_only = True
    )

    class Meta:
        model = UserPost
        fields = ["id", "description", "images", "uploaded_images"]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        userpost = UserPost.objects.create(**validated_data)
        for image in uploaded_images:
            newpost_image = PostImage.objects.create(userpost=userpost, image=image)

        return userpost

    def update(self, instance, validated_data):
        validated_data.pop('uploaded_images', None)
        return super().update(instance, validated_data)

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super(MyTokenObtainPairSerializer, cls).get_token(user)

#         token['user'] = UserSerializer(user).data
#         return token

class MyTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['user'] = UserSerializer(user).data
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user"] = UserSerializer(self.user).data

        update_last_login(None, self.user)

        return data

class OAuth2ObtainPairSerializer(serializers.Serializer):
    id_token = serializers.CharField()
    user = UserSerializer(required=False)

    def google_validate_id_token(self, id_token: str) -> bool:
        response = requests.get(
            settings.GOOGLE_ENDPOINT,
            params={'id_token': id_token}
        )
        if not response.ok:
            raise ValidationError('id_token is invalid.')
        audience = response.json()['aud']
        if audience != settings.GOOGLE_OAUTH2_CLIENT_ID:
            raise ValidationError('Invalid audience.')
        if 'email' not in response.json():
            raise ValidationError('Google response succeed but does not inlcude a valid email, wtf')
        return response.json()

    def get_token(self, user):
        token = RefreshToken.for_user(user)
        token['user'] = UserSerializer(user).data
        return token

    def validate(self, attrs):
        res = self.google_validate_id_token(attrs['id_token'])
        user_param = attrs.get("user", None)
        if not User.objects.filter(username=res['email']).exists():
            if user_param:
                user_param['email'] = res['email']
                user_serializer = UserSerializer(data=user_param)
                if user_serializer.is_valid():
                    user_serializer.save()
                    user = user_serializer.data
                else:
                    return user_serializer.errors
                user, created = User.objects.get_or_create(username=user["email"])
            else:
                user, created = User.objects.get_or_create(username=res["email"], email=res["email"])
                Profile.objects.create(user=user)
        else:
            user, created = User.objects.get_or_create(username=res["email"])


        data = {}
        refresh = self.get_token(user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user"] = UserSerializer(user).data

        update_last_login(None, user)

        return data







        


