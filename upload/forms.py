from django import forms
from .models import Document, Subject, Assignment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model 
import os

User = get_user_model()

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'description', 'deadline', 'number', 'max_points', 'max_uploads']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
        }
    
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.py']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

class TestFileForm(forms.Form):
    test_file = forms.FileField(
        label='Select Test File',
        validators=[validate_file_extension],
        help_text='Upload a Python (.py) test file following the naming convention.'
    )