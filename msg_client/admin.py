from django.contrib import admin

from .models import Message, Client

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    list_filter = ('email',)
    search_fields = ('email',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('topic',)
    search_fields = ('topic',)

