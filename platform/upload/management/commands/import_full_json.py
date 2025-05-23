import json
import os
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from upload.models import Subject, Assignment, Document

class Command(BaseCommand):
    help = 'Import full JSON data dump including users, subjects, assignments and documents'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file dump')

    def handle(self, *args, **options):
        json_file = options['json_file']
        if not os.path.exists(json_file):
            raise CommandError(f"File {json_file} does not exist")
        
        self.stdout.write(f"Importing data from {json_file}...")
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            raise CommandError("The JSON file should contain a list of objects.")
        
        users_data = [obj for obj in data if obj.get('model') == 'auth.user']
        for user_obj in users_data:
            fields = user_obj.get('fields', {})
            user_id = user_obj.get('pk')
            defaults = {
                'username': fields.get('username'),
                'password': fields.get('password'),
                'first_name': fields.get('first_name', ''),
                'last_name': fields.get('last_name', ''),
                'email': fields.get('email', ''),
                'is_superuser': fields.get('is_superuser', False),
                'is_staff': fields.get('is_staff', False),
                'is_active': fields.get('is_active', True),
                'date_joined': fields.get('date_joined'),
            }
            user, created = User.objects.update_or_create(
                id=user_id,
                defaults=defaults
            )
            if created:
                self.stdout.write(f"Created user: {user.username}")
            else:
                self.stdout.write(f"Updated user: {user.username}")
        subjects_data = [obj for obj in data if obj.get('model') == 'upload.subject']
        for subj_obj in subjects_data:
            fields = subj_obj.get('fields', {})
            subject, created = Subject.objects.update_or_create(
                id=subj_obj.get('pk'),
                defaults={
                    'name': fields.get('name'),
                    'description': fields.get('description', '')
                }
            )
            if created:
                self.stdout.write(f"Created subject: {subject.name}")
            else:
                self.stdout.write(f"Updated subject: {subject.name}")
        
        assignments_data = [obj for obj in data if obj.get('model') == 'upload.assignment']
        for assign_obj in assignments_data:
            fields = assign_obj.get('fields', {})
            try:
                subject = Subject.objects.get(pk=fields.get('subject'))
            except Subject.DoesNotExist:
                self.stdout.write(f"Subject with id {fields.get('subject')} not found. Skipping assignment {fields.get('name')}.")
                continue

            deadline_str = fields.get('deadline')
            deadline = None
            if deadline_str:
                try:
                    deadline = datetime.datetime.strptime(deadline_str, '%Y-%m-%d').date()
                except ValueError:
                    self.stdout.write(f"Invalid date format for assignment {fields.get('name')}. Skipping.")
                    continue

            assignment, created = Assignment.objects.update_or_create(
                id=assign_obj.get('pk'),
                defaults={
                    'subject': subject,
                    'name': fields.get('name'),
                    'description': fields.get('description'),
                    'deadline': deadline,
                    'number': fields.get('number'),
                    'max_points': fields.get('max_points', 10),
                    'max_uploads': fields.get('max_uploads', 20)
                }
            )
            if created:
                self.stdout.write(f"Created assignment: {assignment.name}")
            else:
                self.stdout.write(f"Updated assignment: {assignment.name}")
        
        documents_data = [obj for obj in data if obj.get('model') == 'upload.document']
        for doc_obj in documents_data:
            fields = doc_obj.get('fields', {})
            try:
                user = User.objects.get(pk=fields.get('user'))
            except User.DoesNotExist:
                self.stdout.write(f"User with id {fields.get('user')} not found. Skipping document with pk={doc_obj.get('pk')}.")
                continue

            try:
                assignment = Assignment.objects.get(pk=fields.get('assignment'))
            except Assignment.DoesNotExist:
                self.stdout.write(f"Assignment with id {fields.get('assignment')} not found. Skipping document with pk={doc_obj.get('pk')}.")
                continue

            file_rel_path = fields.get('document')
            if not file_rel_path:
                self.stdout.write(f"No document path provided for document pk={doc_obj.get('pk')}. Skipping.")
                continue

            full_path = os.path.join(settings.MEDIA_ROOT, file_rel_path)
            if not os.path.exists(full_path):
                self.stdout.write(f"File {full_path} not found on disk. Skipping document with pk={doc_obj.get('pk')}.")
                continue

            with open(full_path, 'rb') as file:
                file_content = file.read()
            original_filename = os.path.basename(file_rel_path)
            content_file = ContentFile(file_content, name=original_filename)
            document, created = Document.objects.update_or_create(
                id=doc_obj.get('pk'),
                defaults={
                    'assignment': assignment,
                    'user': user,
                    'description': fields.get('description', ''),
                    'document': content_file,
                    'test_result': fields.get('test_result', ''),
                    'grade': fields.get('grade', 0)
                }
            )
            if created:
                self.stdout.write(f"Created document for user {user.username} for assignment {assignment.name}")
            else:
                self.stdout.write(f"Updated document for user {user.username} for assignment {assignment.name}")
        
        self.stdout.write(self.style.SUCCESS("Data import completed successfully."))
