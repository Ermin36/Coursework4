from django.urls import path

from .apps import UsersConfig
from .views import RegistrationView, CustomLoginView, CustomLogoutView, CustomUserList, UserBlockToggleView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('users/list/', CustomUserList.as_view(), name='users_list'),
    path('users/<int:pk>/block/', UserBlockToggleView.as_view(), name='user_block'),
]