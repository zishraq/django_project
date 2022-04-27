# Generated by Django 4.0.2 on 2022-04-27 13:49

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OTPmodel',
            fields=[
                ('otp_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('otp', models.CharField(max_length=100)),
                ('student_id', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('expired_at', models.DateTimeField()),
                ('is_successful', models.BooleanField(default=False)),
            ],
        ),
    ]
