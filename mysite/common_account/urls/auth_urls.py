from django.urls import path
from common_account.views import auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    path('login/',auth_views.CustomTokenObtainPairView.as_view(), name = 'login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('singnup/', auth_views.Singnup.as_view(), name = 'singup'),
  
]
