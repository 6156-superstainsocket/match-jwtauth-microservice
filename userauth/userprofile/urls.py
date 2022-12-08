from django.urls import re_path, path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    re_path(r'register/$', views.RegisterUser.as_view()),
    re_path(r'(?P<user_id>[0-9]+)$', views.ShowUser.as_view()),
    re_path(r'batch$', views.BatchUser.as_view()),
    path('login/', views.CustomAuthToken.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)