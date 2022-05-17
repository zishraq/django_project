# Generated by Django 4.0.2 on 2022-05-17 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BroadcastNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('broadcast_at', models.DateTimeField()),
                ('sent', models.BooleanField(default=False)),
                ('link', models.TextField(default=None, null=True)),
                ('notification_to', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-broadcast_at'],
            },
        ),
    ]