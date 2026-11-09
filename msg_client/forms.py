from django import forms

from msg_client.models import Client, Message


# Create your forms here.

#Clients
class ClientForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Имя',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя'
        })
    )
    last_name = forms.CharField(
        label='Фамилия',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите фамилию'
        })
    )
    middle_name = forms.CharField(
        label='Отчество',
        max_length=100,
        required=False,  # важно: отчество необязательно
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите отчество (необязательно)'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.com'
        })
    )
    comment = forms.CharField(
        label='Комментарий',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Любые примечания о клиенте'
        })
    )

    class Meta:
        model = Client
        fields = ('email', 'first_name','last_name', 'middle_name', 'comment')


#Messages
class MessageForm(forms.ModelForm):
    topic = forms.CharField(
        label='Тема',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите тему письма'
        })
    )
    description = forms.CharField(
        label='Текст сообщения',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Введите текст письма'
        })
    )
    class Meta:
        model = Message
        fields = ('topic', 'description')