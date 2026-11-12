from django.urls import path
from django.contrib.auth import views as auth_views

from .apps import UsersConfig
from .views import RegistrationView, CustomLoginView, CustomLogoutView, CustomUserList, UserBlockToggleView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('users/list/', CustomUserList.as_view(), name='users_list'),
    path('users/<int:pk>/block/', UserBlockToggleView.as_view(), name='user_block'),

    #Reset Password
    path('password-reset/', auth_views.PasswordResetView.as_view(
            template_name='reset_password/password_reset_form.html',
            email_template_name='reset_password/password_reset_email.html',
            subject_template_name='reset_password/password_reset_subject.txt',
            success_url='/password-reset/done/',
        ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='reset_password/password_reset_done.html',
    ), name='password_reset_done'),

    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='reset_password/password_reset_confirm.html',
        success_url='/users/password-reset/complete/',
    ), name='password_reset_confirm'),

    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='reset_password/password_reset_complete.html',
    ), name='password_reset_complete'),
]