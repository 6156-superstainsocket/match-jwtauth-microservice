from rest_framework import serializers
from .models import UserPost, PostImage
from django.contrib.auth import get_user_model
import requests
from django.conf import settings
from userprofile.serializers import UserSerializer

User = get_user_model()

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
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserPost
        fields = ["id", "user", "description", "images", "uploaded_images"]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        userpost = UserPost.objects.create(**validated_data)
        for image in uploaded_images:
            newpost_image = PostImage.objects.create(userpost=userpost, image=image)

        return userpost

    def update(self, instance, validated_data):
        validated_data.pop('uploaded_images', None)
        return super().update(instance, validated_data)



