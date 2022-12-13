from django.urls import re_path, path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    re_path(r'register/$', views.RegisterUser.as_view()),
    re_path(r'(?P<user_id>[0-9]+)$', views.ShowUser.as_view()),
    re_path(r'batch$', views.BatchUser.as_view()),
    path('login/', views.CustomAuthToken.as_view()),
    path('token/', views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('oauth2/', views.MyOAuth2TokenPairView.as_view(), name='oauth2'),
]

urlpatterns = format_suffix_patterns(urlpatterns)