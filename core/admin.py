from django.contrib import admin

# Register your models here.
from chat.models import Message, Chat


@admin.register(Message)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'date')

@admin.register(Chat)
class MessagesAdmin(admin.ModelAdmin):
    pass
