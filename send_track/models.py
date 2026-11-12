from django.db import models
from django.utils import timezone

from msg_client.models import Message, Client
from users.models import CustomUser


# Create your models here.
class Mailing(models.Model):

    STATUS_CHOICES = (
        ('created', 'Создана'),
        ('launched', 'Запущена'),
        ('completed', 'Завершена'),
        ('stopped', 'Оключена')
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, default='created', max_length=20, verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    recipients = models.ManyToManyField(Client, related_name='mailings', verbose_name='Получатели')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Создатель')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    def clean(self):
        if self.start_time and self.end_time:
            if timezone.now() < self.start_time:
                self.status = 'created'
            elif timezone.now() > self.start_time:
                self.status = 'launched'
            elif timezone.now() > self.end_time:
                self.status = 'completed'

        super().clean()

    def update_status(self):
        """Пересчитывает статус по текущему времени и сохраняет в базе, если он изменился."""
        now = timezone.now()

        if not self.is_active:
            new_status = 'stopped'
        elif now < self.start_time:
            new_status = 'created'
        elif now > self.end_time:
            new_status = 'completed'
        else:
            new_status = 'launched'

        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=['status'])

        return self.status

    @property
    def progress_percent(self):
        if not self.start_time or not self.end_time or self.end_time <= self.start_time:
            return 0
        total = (self.end_time - self.start_time).total_seconds()
        elapsed = (timezone.now() - self.start_time).total_seconds()
        return max(0, min(100, elapsed / total * 100))

    @property
    def dynamic_status(self):
        now = timezone.now()
        if now < self.start_time:
            return 'created'
        if now > self.end_time:
            return 'completed'
        return 'launched'

    @property
    def dynamic_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.dynamic_status, '')


    def __str__(self):
        return f'ID: {self.pk}. Status: {self.status}'

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ('view_all_mailings', 'Может просматривать все рассылки'),
            ('disable_mailing', 'Может отключать рассылки'),
        ]


class MailingAttempt(models.Model):

    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=(
        ('ok', 'Успешно'),
        ('error', 'Не успешно')
    ))
    server_response = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.attempt_time}: {self.status}'

    class Meta:
        verbose_name = 'Статус рассылки'
        verbose_name_plural = 'Статусы рассылок'
        permissions = [
            ('view_all_mailingattempts', 'Может просматривать все попытки'),
        ]
