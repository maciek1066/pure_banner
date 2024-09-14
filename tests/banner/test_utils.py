import django
django.setup()

import unittest
from unittest.mock import patch

import requests
from django.core.exceptions import ValidationError
from banner.utils import fetch_photos_from_api, download_image, generate_unique_filename


class TestUtils(unittest.TestCase):

    @patch('banner.utils.requests.get')
    def test_fetch_photos_from_api_success(self, mock_get):
        # Mock successful API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "success": True,
            "photos": [{"id": 1, "title": "Test Photo"}]
        }

        photos = fetch_photos_from_api()
        self.assertEqual(len(photos), 1)
        self.assertEqual(photos[0]["title"], "Test Photo")

    @patch('banner.utils.requests.get')
    def test_fetch_photos_from_api_failure(self, mock_get):
        # Mock failed API response
        mock_get.return_value.status_code = 500
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError

        with self.assertRaises(ValidationError):
            fetch_photos_from_api()

    @patch('banner.utils.requests.get')
    def test_download_image_success(self, mock_get):
        # Mock successful image download
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b'fake_image_content'

        content_file = download_image("http://example.com/photo.jpg")
        self.assertEqual(content_file.read(), b'fake_image_content')

    @patch('banner.utils.requests.get')
    def test_download_image_failure(self, mock_get):
        # Mock failed image download
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError

        with self.assertRaises(ValidationError):
            download_image("http://example.com/photo.jpg")

    def test_generate_unique_filename(self):
        unique_filename = generate_unique_filename("photo.jpg")
        self.assertTrue(unique_filename.endswith(".jpg"))
