from django.contrib import admin
from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('is_google', 'name', 'phone', 'iconid')
    list_per_page = 10
    list_filter = ('is_google', )

admin.site.register(Profile, ProfileAdmin)
