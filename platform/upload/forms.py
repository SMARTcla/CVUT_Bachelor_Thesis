from django import forms
from .models import Document, Subject, Assignment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import os

User = get_user_model()

# Validator to reject any HTML/XML tags
no_html_validator = RegexValidator(
    regex=r"\A(?!.*<[^>]+>).*\Z",
    message="HTML or XML tags are not allowed.",
    code="invalid_html",
    flags=forms.re.DOTALL
)

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
    # enforce no HTML in name and description
    name = forms.CharField(validators=[no_html_validator])
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        validators=[no_html_validator]
    )

    class Meta:
        model = Subject
        fields = ['name', 'description']

class AssignmentForm(forms.ModelForm):
    name = forms.CharField(validators=[no_html_validator])
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        validators=[no_html_validator]
    )

    class Meta:
        model = Assignment
        fields = ['name', 'description', 'deadline', 'number', 'max_points', 'max_uploads']

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
