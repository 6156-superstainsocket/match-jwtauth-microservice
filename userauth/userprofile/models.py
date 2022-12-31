from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver #add this
from django.db.models.signals import post_save #add this

# from django.conf import settings
# from rest_framework.authtoken.models import Token

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


# Create your models here.
    
class Profile(models.Model):
    is_google = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default="")
    phone = models.CharField(max_length=20, default="")
    description = models.CharField(max_length=140, default="")
    iconid = models.IntegerField(null=True, default=0)
    icon = models.ImageField(upload_to="icons", blank=True, null=True, default="default_icon.jpg")

    '''
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    '''

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('model-user-detail', args=[str(self.id)])
