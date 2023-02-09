# Generated by Django 4.1.5 on 2023-02-09 15:18

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
            name='AddProject',
            fields=[
                ('username', models.CharField(max_length=100)),
                ('project_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('name', models.TextField(default='')),
                ('category', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('name', models.CharField(default='', max_length=100)),
                ('text', models.TextField(default='')),
                ('files', models.FileField(upload_to='results')),
                ('project_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.project')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('description', models.TextField(default='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('business_username', models.CharField(max_length=100)),
                ('student_username', models.CharField(max_length=100)),
                ('text', models.TextField(default='')),
                ('result', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.result')),
            ],
        ),
    ]