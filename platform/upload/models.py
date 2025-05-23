# upload/models.py

from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta
import os
from django.core.exceptions import ValidationError
import markdown
from django.utils.html import mark_safe

def document_upload_path(instance, filename):
    username = instance.user.username
    subject_name = instance.assignment.subject.name
    assignment_no = instance.assignment.number
    return f"{username}/{subject_name}/{assignment_no}/{filename}"
    
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.py']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    number = models.PositiveIntegerField()
    max_points = models.PositiveIntegerField(default=10, help_text="Maximum points for this assignment.")
    max_uploads = models.PositiveIntegerField(default=20, help_text="Maximum number of downloads for a student.")

    def __str__(self):
        return self.name

    def get_description_markdown(self):
        return mark_safe(markdown.markdown(self.description))

class Document(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='documents')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(
        upload_to=document_upload_path,
        validators=[validate_file_extension]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    test_result = models.TextField(blank=True, null=True)
    grade = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.description or self.document.name