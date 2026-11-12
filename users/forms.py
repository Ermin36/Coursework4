from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import CustomUser

# Create your forms here.

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'image', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget_class = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs['class'] = widget_class + ' bg-black text-white border-secondary'


class CustomUserAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email адрес',
        widget=forms.EmailInput(attrs={'autofocus': True}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control bg-black text-white border-secondary'

    error_messages = {
        'invalid_login': 'Неверный email или пароль.',
        'inactive': 'Аккаунт заблокирован. Обратитесь к администратору.',
    }

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )