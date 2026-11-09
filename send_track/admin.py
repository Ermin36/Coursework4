from django.contrib import admin

from .models import Mailing, MailingAttempt

# Register your models here.
@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('status', 'pk')
    list_filter = ('status',)
    search_fields = ('status', 'pk')

    exclude = ('status',)

@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('status', 'pk', 'attempt_time', 'mailing')
    list_filter = ('status', )
    search_fields = ('status', 'attempt_time', 'pk')

    exclude = ('status',)


