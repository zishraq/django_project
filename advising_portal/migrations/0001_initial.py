# Generated by Django 4.0.2 on 2022-03-25 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('course_code', models.CharField(max_length=10)),
                ('course_title', models.TextField()),
                ('credit', models.FloatField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('faculty_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('initials', models.TextField()),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(max_length=10)),
                ('grade_point', models.FloatField()),
                ('maximum', models.FloatField()),
                ('minimum', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='RoutineSlot',
            fields=[
                ('routine_id', models.IntegerField(primary_key=True, serialize=False)),
                ('routine', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('time_slot_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('day', models.CharField(max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('advisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='advising_portal.faculty')),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('semester_id', models.IntegerField(primary_key=True, serialize=False)),
                ('semester_name', models.TextField()),
                ('semester_starts_on', models.DateField()),
                ('semester_ends_on', models.DateField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('advising_status', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('section_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('section_no', models.PositiveIntegerField(default=1)),
                ('section_capacity', models.PositiveIntegerField(default=0)),
                ('total_students', models.PositiveIntegerField(default=0)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='advising_portal.course')),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='advising_portal.faculty')),
                ('routine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='advising_portal.routineslot')),
            ],
        ),
        migrations.AddField(
            model_name='routineslot',
            name='time_slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advising_portal.timeslot'),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('department_name', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CoursesTaken',
            fields=[
                ('course_record_id', models.AutoField(primary_key=True, serialize=False)),
                ('grade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='advising_portal.grade')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='advising_portal.section')),
                ('semester', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='advising_portal.semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advising_portal.student')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='advising_portal.department'),
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisite_course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='advising_portal.course'),
        ),
    ]
