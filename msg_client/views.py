from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from msg_client.forms import MessageForm, ClientForm
from msg_client.models import Client, Message
from users.views import ManagerMixin


# Create your views here.
#Clients
class ClientListView(ManagerMixin, ListView):
    owner = 'created_by'
    perms = ('msg_client.view_all_clients',)
    model = Client
    template_name = 'client/list.html'
    context_object_name = 'clients'

class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'client/detail.html'
    context_object_name = 'client'

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/create.html'
    success_url = reverse_lazy('msg_client:client_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/update.html'
    success_url = reverse_lazy('msg_client:client_list')

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'client/delete.html'
    success_url = reverse_lazy('msg_client:client_list')


#Messages
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'message/list.html'
    context_object_name = 'messages'

class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'message/detail.html'
    context_object_name = 'message'

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'message/create.html'
    success_url = reverse_lazy('msg_client:message_list')

class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'message/update.html'
    context_object_name = 'message'

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'message/delete.html'
    success_url = reverse_lazy('msg_client:message_list')