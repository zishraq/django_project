# Generated by Django 4.0.2 on 2022-03-23 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advising_portal', '0010_delete_coursestaken'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoursesTaken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='advising_portal.grade')),
                ('section_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='advising_portal.section')),
                ('semester_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='advising_portal.semester')),
                ('student_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='advising_portal.student')),
            ],
        ),
    ]
