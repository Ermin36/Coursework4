from django.urls import reverse_lazy
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
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('send_track:home')

class CustomLogoutView(LogoutView):
    #template_name = 'logout.html'
    next_page = reverse_lazy('send_track:home')