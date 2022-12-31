from django.contrib import admin
from .models import UserPost

# Register your models here.

class UserPostAdmin(admin.ModelAdmin):
    list_display = ('description', 'user')
    list_per_page = 10
    
admin.site.register(UserPost, UserPostAdmin)

