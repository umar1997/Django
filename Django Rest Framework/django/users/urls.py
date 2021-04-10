from django.urls import path
from .views import CustomUserCreate, CustomUserRegister, BlacklistTokenView

app_name = 'users'

urlpatterns = [
    # For OAuth
    # path('create/', CustomUserCreate.as_view(), name="create_user"),
    # For JWT
    path('register/', CustomUserRegister.as_view(), name="register_user"),
    # For JWT BlackList 
    path('logout/blacklist/', BlacklistTokenView.as_view(), name='blacklist')
]
