from django.db import models

# Create your models here.
class Message(models.Model):
    topic = models.CharField(max_length=200)
    body = models.TextField()

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Client(models.Model):
    email = models.EmailField(max_length=200)
    fio = models.CharField(max_length=300)
    comment = models.TextField()

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
