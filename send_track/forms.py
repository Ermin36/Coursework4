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

    def clean_end_time(self):
        end_time = self.cleaned_data['end_time']
        start_time = self.cleaned_data['start_time']

        if end_time < start_time:
            raise forms.ValidationError(
                'Время окончания должно быть позже времени начала.'
            )
        return end_time

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = Mailing
        fields = ('start_time', 'end_time', 'message', 'recipients')
