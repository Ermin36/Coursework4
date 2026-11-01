from django.db import models

from msg_client.models import Message, Client


# Create your models here.
class Mailing(models.Model):

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(choices=(
        ('created', 'Создана'),
        ('launched', 'Запущена'),
        ('completed', 'Завершена')
    ))
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Client, related_name='mailings', verbose_name='Получатели')

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class MailingAttempt(models.Model):

    attempt_time = models.DateTimeField()
    status = models.CharField(choices=(
        ('ok', 'Успешно'),
        ('error', 'Не успешно')
    ))
    server_response = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Статус рассылки'
        verbose_name_plural = 'Статусы рассылок'
