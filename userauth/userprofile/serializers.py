from rest_framework import serializers
from .models import Profile
from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):

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

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')

        user = User.objects.create_user(username=validated_data['username'],
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

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # 添加额外信息
        token['user'] = UserSerializer(user).data
        return token








        


