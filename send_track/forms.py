from django import forms
from django.utils import timezone

from .models import Mailing, MailingAttempt
from msg_client.models import Client, Message


# Create your forms here.
#Mailings
class MailingForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        label='Время начала',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end_time = forms.DateTimeField(
        label='Время окончания',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    message = forms.ModelChoiceField(
        queryset=Message.objects.all(),
        label='Сообщение',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    recipients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(),
        label='Получатели',
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 6})
    )

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time <= timezone.now():
            raise forms.ValidationError(
                'Время начала не может быть в прошлом. Укажите текущее или будущее время.'
            )
        return start_time

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if end_time <= start_time:
                self.add_error('end_time', 'Время окончания должно быть позже времени начала.')

        return cleaned_data

    class Meta:
        model = Mailing
        fields = ('start_time', 'end_time', 'message', 'recipients')

#MailingAttempts
class MailingAttemptForm(forms.ModelForm):
    attempt_time = forms.DateTimeField(
        label='Время попытки',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    status = forms.ChoiceField(
        label='Статус',
        choices=MailingAttempt._meta.get_field('status').choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    server_response = forms.CharField(
        label='Ответ сервера',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    mailing = forms.ModelChoiceField(
        queryset=Mailing.objects.all(),
        label='Рассылка',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = MailingAttempt
        fields = ('attempt_time', 'status', 'server_response', 'mailing')