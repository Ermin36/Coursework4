from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserAuthenticationForm


# Create your views here.
class RegistrationView(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('send_track:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomUserAuthenticationForm
    success_url = reverse_lazy('send_track:home')

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('send_track:home')


class CustomLogoutView(LogoutView):
    #template_name = 'logout.html'
    next_page = reverse_lazy('send_track:home')


class ManagerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Доступ только для менеджеров и суперпользователей."""

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='Manager').exists()


class CustomUserList(ManagerRequiredMixin, ListView):
    model = CustomUser
    template_name = 'user/list.html'
    context_object_name = 'users'


class UserBlockToggleView(ManagerRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)

        # Нельзя заблокировать суперпользователя или самого себя
        if not user.is_superuser and user != request.user:
            user.is_active = not user.is_active
            user.save(update_fields=['is_active'])

        return redirect('users:users_list')
