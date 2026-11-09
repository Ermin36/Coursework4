from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from msg_client.forms import MessageForm, ClientForm
from msg_client.models import Client, Message


# Create your views here.
#Clients
class ClientListView(ListView):
    model = Client
    template_name = 'client/list.html'
    context_object_name = 'clients'

class ClientDetailView(DetailView):
    model = Client
    template_name = 'client/detail.html'
    context_object_name = 'client'

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/create.html'
    success_url = reverse_lazy('msg_client:clients')

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/update.html'
    success_url = reverse_lazy('msg_client:clients')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'client/delete.html'
    success_url = reverse_lazy('msg_client:clients')


#Messages
class MessageListView(ListView):
    model = Message
    template_name = 'message/list.html'
    context_object_name = 'messages'

class MessageDetailView(DetailView):
    model = Message
    template_name = 'message/detail.html'
    context_object_name = 'message'

class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'message/create.html'
    success_url = reverse_lazy('msg_client:messages')

class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'message/update.html'
    context_object_name = 'message'

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'message/delete.html'
    success_url = reverse_lazy('msg_client:messages')