# Generated by Django 4.0.2 on 2022-05-11 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advising_portal', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sectionsrequested',
            name='is_approved_by_advisor',
        ),
        migrations.RemoveField(
            model_name='sectionsrequested',
            name='is_approved_by_chairman',
        ),
        migrations.RemoveField(
            model_name='sectionsrequested',
            name='is_approved_by_instructor',
        ),
        migrations.AddField(
            model_name='sectionsrequested',
            name='advisor_approval_status',
            field=models.CharField(choices=[('pending', 'pending'), ('pending', 'pending'), ('pending', 'pending')], default='pending', max_length=10),
        ),
        migrations.AddField(
            model_name='sectionsrequested',
            name='chairman_approval_status',
            field=models.CharField(choices=[('pending', 'pending'), ('pending', 'pending'), ('pending', 'pending')], default='pending', max_length=10),
        ),
        migrations.AddField(
            model_name='sectionsrequested',
            name='instructor_approval_status',
            field=models.CharField(choices=[('pending', 'pending'), ('pending', 'pending'), ('pending', 'pending')], default='pending', max_length=10),
        ),
    ]
