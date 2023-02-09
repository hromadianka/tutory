from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    email = models.EmailField()
    description = models.TextField(default='')
    name = models.TextField(default='')

    def __str__(self):
        return self.user.username

class Project(models.Model):
     id = models.UUIDField(primary_key=True, default=uuid.uuid4)
     user = models.CharField(max_length=100)
     name = models.TextField(default='')
     category = models.CharField(max_length=100)
     description = models.TextField(null=True)

     def __str__(self):
        return str(self.id)

class AddProject(models.Model):
    username = models.CharField(max_length=100)
    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    def __str__(self):
        return str(self.id)

class Result(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=100, unique=False)
    project_id = models.ForeignKey(Project, on_delete = models.SET_NULL, null=True)
    name = models.CharField(max_length=100, default='')
    text = models.TextField(default='')
    files = models.FileField (upload_to='results')

    def __str__(self):
        return str(self.username)

class Feedback(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    business_username = models.CharField(max_length=100)
    student_username = models.CharField(max_length=100)
    result = models.ForeignKey(Result, on_delete = models.SET_NULL, name="result", null=True)
    text = models.TextField(default='')

    def __str__(self):
        return str(self.text)
