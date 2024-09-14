
from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import path

from banner.models import Chat, Message
from banner.utils import send_first_unsent_photo


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send-photo/', self.send_photo_action, name='send_photo_action'),
        ]
        return custom_urls + urls

    def send_photo_action(self, request):
        """Custom admin action to send photo to all chats."""
        try:
            result = send_first_unsent_photo()
            self.message_user(request, result, messages.SUCCESS)
        except ValidationError as e:
            self.message_user(request, e.message, messages.ERROR)
        return redirect('..')

    def changelist_view(self, request, extra_context=None):
        """Override changelist_view to include a custom button for sending photos."""
        extra_context = extra_context or {}
        extra_context['send_photo_url'] = 'send-photo/'  # Add the URL for the custom action
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'external_photo_id', 'image')
    search_fields = ('text', 'external_photo_id')
    list_filter = ('external_photo_id',)
