from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from accounts.api.views import RegisterAPIView, ProfileRUDAPIView

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterAPIView.as_view(), name="register"),
    path('profile/update/<slug>/', ProfileRUDAPIView.as_view(), name='profile_update'),
]