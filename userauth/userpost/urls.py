from django.urls import re_path, path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    re_path(r'(?P<pk>[0-9]+)/$', views.UserPostDetail.as_view()),
    re_path(r'user/(?P<user_id>[0-9]+)/', views.UserPostList.as_view()),
    path('addpost/', views.UserPostAdd.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)