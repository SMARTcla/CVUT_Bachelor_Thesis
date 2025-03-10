# upload/models.py

from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta
import os
from django.core.exceptions import ValidationError
import markdown
from django.utils.html import mark_safe

def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.py']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()  # Added description field

    def __str__(self):
        return self.name

class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    number = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name

    def get_description_markdown(self):
        return mark_safe(markdown.markdown(self.description))

class Document(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='documents')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    test_result = models.CharField(max_length=255, blank=True, null=True)  # Field to store test results
    grade = models.PositiveIntegerField(default=0)  # Added grade field

    def __str__(self):
        return self.description or self.document.name
