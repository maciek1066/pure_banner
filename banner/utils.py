import requests

from typing import List, Dict, Union

import uuid
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError

from banner.models import Message, Chat


def fetch_photos_from_api(offset: int = 0, limit: int = 10) -> List[Dict[str, Union[int, str]]]:
    """Fetches photos from the API with pagination."""
    api_url = "https://api.slingacademy.com/v1/sample-data/photos"
    try:
        response = requests.get(f"{api_url}?offset={offset}&limit={limit}", timeout=30)
        response.raise_for_status()
        data = response.json()

        if not data.get("success"):
            raise ValidationError("API response was not successful.")

        return data.get("photos", [])  # Return list of photos

    except requests.RequestException as e:
        raise ValidationError(f"Error fetching photos from API: {str(e)}")


# Define a function to download an image from a URL
def download_image(photo_url: str) -> ContentFile:
    """Downloads an image from the external URL and returns it as a file."""
    try:
        response = requests.get(photo_url)
        response.raise_for_status()
        return ContentFile(response.content)  # Returns the file as a ContentFile object
    except requests.RequestException as e:
        raise ValidationError(f"Error downloading image from {photo_url}: {str(e)}")


def generate_unique_filename(original_name: str) -> str:
    """Generates a unique filename for the file."""
    extension = original_name.split('.')[-1]
    unique_name = f"{uuid.uuid4()}.{extension}"
    return unique_name


# Define a function to store an image locally and return its URL
def store_image_locally(photo_url: str) -> str:
    """Store the image in external storage and return its URL."""
    image_content = download_image(photo_url)
    file_name = photo_url.split('/')[-1]  # Extract file name from URL
    unique_filename = generate_unique_filename(file_name)
    file_path = f'images/{unique_filename}'
    with default_storage.open(file_path, 'wb') as f:
        f.write(image_content.read())
    return default_storage.url(file_path)  # Return the URL of the stored image


# Define a function to send the first unsent photo to all chats
def send_first_unsent_photo() -> str:
    offset = 0
    limit = 10

    while True:
        # Fetch photos from API
        photos = fetch_photos_from_api(offset=offset, limit=limit)

        if not photos:
            # No more photos available, break the loop
            break

        # Get photo IDs from API and check which ones have been sent
        photo_ids = [photo['id'] for photo in photos]
        sent_photos = set(
            Message.objects.filter(external_photo_id__in=photo_ids).values_list('external_photo_id', flat=True))

        # Find the first photo that has not been sent
        unsent_photos = [photo for photo in photos if photo['id'] not in sent_photos]

        if unsent_photos:
            selected_photo = unsent_photos[0]  # Select the first unsent photo

            # Store the image in external storage
            image_url = store_image_locally(selected_photo["url"])

            # Create a message with the image URL and save it on the server
            message = Message(
                text=selected_photo["description"],
                external_photo_id=selected_photo["id"],
                image=image_url  # Store URL of the image
            )

            # Assign the message to all chats
            chats = Chat.objects.all()
            message.save()
            message.chats.set(chats)

            return f"Successfully sent photo '{selected_photo['title']}' to all chats."

        # Increase offset and fetch more photos if no unsent photos found
        offset += limit

    # If no unsent photos found after checking all available records
    raise ValidationError("No new photos to send.")
