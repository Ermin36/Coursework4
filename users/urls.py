from django.urls import path

from .apps import UsersConfig
from .views import RegistrationView, CustomLoginView, CustomLogoutView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]