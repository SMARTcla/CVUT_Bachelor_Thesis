from django.contrib import admin
from .models import Document, Subject, Assignment

admin.site.register(Document)
admin.site.register(Subject)
admin.site.register(Assignment)