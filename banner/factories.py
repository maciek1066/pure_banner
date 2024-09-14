import factory

from banner.models import Message, Chat, UserProfile


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    uuid = factory.Faker('uuid4')


class ChatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Chat

    user = factory.SubFactory(UserProfileFactory)
    created_at = factory.Faker('date_time')


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    text = factory.Faker('text')
    external_photo_id = factory.Faker('uuid4')
    image = factory.django.ImageField()
