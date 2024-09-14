# Generated by Django 4.2.16 on 2024-09-14 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('external_photo_id', models.IntegerField(unique=True)),
                ('image', models.ImageField(upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banner.chat')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banner.message')),
            ],
            options={
                'unique_together': {('chat', 'message')},
            },
        ),
        migrations.AddField(
            model_name='chat',
            name='messages',
            field=models.ManyToManyField(related_name='chats', through='banner.ChatMessage', to='banner.message'),
        ),
        migrations.AddField(
            model_name='chat',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='banner.userprofile'),
        ),
    ]
