from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterUserView,
    ProfileView,
    ChangePasswordView,
    CustomTokenObtainPairView,

    RequestPasswordResetEmailView,
    PasswordTokenCheckAPIView,
    SetNewPasswordAPIView
)

app_name = 'User'

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name="register_user"),
    path('profile/<str:pk>/', ProfileView.as_view(), name='get_profile'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login_user'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),

    # Password Reset Email
    path('reset-email/', RequestPasswordResetEmailView.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPIView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete')
]