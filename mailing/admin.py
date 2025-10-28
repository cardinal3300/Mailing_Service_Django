from django.contrib import admin
from .models import Recipient, Message, Mailing


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('message', 'status', 'send_time', 'recipients', 'end_time', 'owner')
    list_filter = ('status',)
    search_fields = ('message__subject',)

    def recipients(self, obj):
        return ", ".join([r.name for r in obj.recipients.all()])

    recipients.short_description = "Получатели"
