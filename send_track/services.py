from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Mailing, MailingAttempt


def _send_to_client(mailing, client):
    """Отправляет письмо одному клиенту и записывает попытку. Возвращает True/False."""
    try:
        send_mail(
            subject=mailing.message.topic,
            message=mailing.message.description,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[client.email],
            fail_silently=False,
        )
        MailingAttempt.objects.create(
            attempt_time=timezone.now(),
            status='ok',
            server_response='Письмо успешно отправлено',
            mailing=mailing,
            client=client,
        )
        return True
    except Exception as e:
        MailingAttempt.objects.create(
            attempt_time=timezone.now(),
            status='error',
            server_response=str(e),
            mailing=mailing,
        )
        return False


def send_mailing(mailing):
    """
    Отправляет письма получателям одной рассылки.
    Проверяет период активности.

    Возвращает словарь с итогами:
    {'sent': 5, 'failed': 1, 'skipped': 'вне периода' — или None}
    """
    now = timezone.now()

    # Проверка периода: рассылка должна быть активна
    if not (mailing.start_time <= now <= mailing.end_time):
        return {'sent': 0, 'failed': 0, 'skipped': True}

    sent = 0
    failed = 0

    for client in mailing.recipients.all():
        if _send_to_client(mailing, client):
            sent += 1
        else:
            failed += 1

    # Актуализируем статус: если период кончился, рассылка станет «Завершена»
    mailing.update_status()

    return {'sent': sent, 'failed': failed, 'skipped': None}


def send_active_mailings():
    """
    Отправляет письма по всем активным рассылкам.
    Подходит и для кнопки «Отправить все», и для периодического запуска
    (команда/планировщик).

    Возвращает сводку: {'processed': 3, 'sent': 12, 'failed': 2, 'skipped': 1}
    """
    now = timezone.now()

    mailings = Mailing.objects.filter(
        start_time__lte=now,
        end_time__gte=now,
    ).prefetch_related('recipients')

    result = {'processed': 0, 'sent': 0, 'failed': 0, 'skipped': 0}

    for mailing in mailings:
        outcome = send_mailing(mailing)
        result['processed'] += 1
        result['sent'] += outcome['sent']
        result['failed'] += outcome['failed']
        if outcome['skipped']:
            result['skipped'] += 1

    return result
