from django import forms
from .models import Document, Subject, Assignment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model 
from django.core.exceptions import ValidationError
import os
import re

User = get_user_model()

# ——— Validator to reject any HTML/XML tags ———
NOT_HTML_RE = re.compile(r'\A(?!.*<[^>]+>).*?\Z', re.DOTALL)

def validate_not_html(value):
    """
    Raises ValidationError if the input contains any <tag>…</tag> or standalone <foo>.
    """
    if not NOT_HTML_RE.match(value):
        raise ValidationError("Input may not contain HTML/XML tags.")

# ——— File‐extension validator for .py ———
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.py']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

# ——— Forms ———

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
        # attach our no‐HTML validator to both fields
        validators = {
            'name': [validate_not_html],
            'description': [validate_not_html],
        }


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'description', 'deadline', 'number', 'max_points', 'max_uploads']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
        }
        validators = {
            'name': [validate_not_html],
            'description': [validate_not_html],
        }


class TestFileForm(forms.Form):
    test_file = forms.FileField(
        label='Select Test File',
        validators=[validate_file_extension],
        help_text='Upload a Python (.py) test file following the naming convention.'
    )
