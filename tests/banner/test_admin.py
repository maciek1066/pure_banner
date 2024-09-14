import django
django.setup()

import unittest
from unittest.mock import patch, MagicMock

from django.core.exceptions import ValidationError
from django.test import RequestFactory
from django.contrib import admin, messages
from banner.admin import ChatAdmin
from banner.models import Chat


class TestChatAdmin(unittest.TestCase):

    @patch('banner.admin.send_first_unsent_photo')
    def test_send_photo_action_success(self, mock_send_first_unsent_photo):
        # Mock a successful send
        mock_send_first_unsent_photo.return_value = "Photos sent successfully"

        # Set up request with mock messages framework
        request = RequestFactory().post('/admin/send-photo/')
        request._messages = MagicMock()  # Mock the messages framework

        # Create an instance of ChatAdmin
        admin_instance = ChatAdmin(Chat, admin.site)

        # Call the admin action
        response = admin_instance.send_photo_action(request)

        # Check if the response is a redirect (as expected)
        self.assertEqual(response.status_code, 302)
        # Ensure that the message was added to the request with the correct level
        request._messages.add.assert_called_once_with(messages.SUCCESS, "Photos sent successfully", "")

    @patch('banner.admin.send_first_unsent_photo')
    def test_send_photo_action_validation_error(self, mock_send_first_unsent_photo):
        # Mock a validation error
        mock_send_first_unsent_photo.side_effect = ValidationError("No new photos to send")

        # Set up request with mock messages framework
        request = RequestFactory().post('/admin/send-photo/')
        request._messages = MagicMock()  # Mock the messages framework

        # Create an instance of ChatAdmin
        admin_instance = ChatAdmin(Chat, admin.site)

        # Call the admin action
        response = admin_instance.send_photo_action(request)

        # Check if the response is a redirect (as expected)
        self.assertEqual(response.status_code, 302)
        # Ensure that the error message was added to the request with the correct level
        request._messages.add.assert_called_once_with(messages.ERROR, "No new photos to send", "")
