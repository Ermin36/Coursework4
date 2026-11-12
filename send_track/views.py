from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DetailView, DeleteView, View
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from msg_client.models import Client
from .models import Mailing, MailingAttempt
from .forms import MailingForm
from .services import send_mailing, send_active_mailings

# Create your views here.

class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['total_mailings'] = Mailing.objects.count()
        contex['active_mailings'] = Mailing.objects.filter(
            start_time__lte=timezone.now(),
            end_time__gte=timezone.now()
        ).count()
        contex['total_clients'] = Client.objects.count()

        return contex


#Mailing Send
class MailingSend(LoginRequiredMixin, View):

    def post(self, request, **kwargs):
        pk = kwargs['pk']
        mailing: Mailing = get_object_or_404(Mailing, pk=pk)

        outcome = send_mailing(mailing)

        if outcome['skipped']:
            messages.warning(request, f'Рассылка №{pk} вне периода активности.')
        elif outcome['failed'] == 0:
            messages.success(
                request,
                f'Рассылка №{pk}: отправлено {outcome["sent"]} писем.'
            )
        else:
            messages.warning(
                request,
                f'Рассылка №{pk}: успешных — {outcome["sent"]}, '
                f'с ошибками — {outcome["failed"]}.'
            )

        return redirect('send_track:mailing_detail', pk=pk)


class MailingSendAll(LoginRequiredMixin, View):

    def post(self, request, **kwargs):
        outcome = send_active_mailings()
        if outcome['processed'] == 0:
            messages.info(request, 'Активных рассылок сейчас нет.')
        elif outcome['failed'] == 0:
            messages.success(
                request,
                f'Обработано рассылок: {outcome["processed"]}, '
                f'отправлено писем: {outcome["sent"]}.'
            )
        else:
            messages.warning(
                request,
                f'Отправлено писем: {outcome["sent"]}, '
                f'с ошибками — {outcome["failed"]}.'
            )

        return redirect('send_track:mailing_list')


#Mailing Data
class MailingCreate(LoginRequiredMixin, CreateView):
    template_name = 'mailing/create.html'
    model = Mailing
    form_class = MailingForm
    context_object_name = 'mailing'
    success_url = reverse_lazy('send_track:mailing_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class MailingUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'mailing/update.html'
    model = Mailing
    form_class = MailingForm
    context_object_name = 'mailing'
    success_url = reverse_lazy('send_track:mailing_list')

class MailingDetail(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/detail.html'
    context_object_name = 'mailing'

    def get_object(self, queryset=None):
        obj: Mailing = super().get_object(queryset)
        obj.update_status()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = self.get_object()

        context['total_attempts'] = mailing.attempts.count()
        context['success_attempts'] = mailing.attempts.filter(status='ok').count()
        return context

class MailingDelete(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/delete.html'
    success_url = reverse_lazy('send_track:mailing_list')

class MailingList(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        return super().get_queryset().annotate(
            total_attempts=Count('attempts', distinct=True),
            success_attempts=Count('attempts', filter=Q(attempts__status='ok'), distinct=True),
        )


#MailingAttempt Data
class MailingAttemptDetail(LoginRequiredMixin, DetailView):
    model = MailingAttempt
    template_name = 'mailing_attempt/detail.html'
    context_object_name = 'attempt'

class MailingAttemptDelete(LoginRequiredMixin, DeleteView):
    model = MailingAttempt
    template_name = 'mailing_attempt/delete.html'
    context_object_name = 'mailing_attempt'
    success_url = reverse_lazy('send_track:mailing_attempt_list')

class MailingAttemptList(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailing_attempt/list.html'
    context_object_name = 'mailing_attempts'