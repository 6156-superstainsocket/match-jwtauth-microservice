from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    description = models.CharField(max_length=140, default="")

class PostImage(models.Model):
    userpost = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="post_img", default="", null=True, blank=True)