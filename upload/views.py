# upload/views.py

import importlib.util
import os
import re 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import TestFileForm, DocumentForm, SignUpForm
from .models import Document, Subject, Assignment
from django.contrib import messages

def is_teacher(user):
    return user.is_superuser or user.groups.filter(name='Teachers').exists()

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('upload:subject_list')  # Добавляем неймспейс
        else:
            messages.error(request, "Registration failed. Please check your data.")
    else:
        form = SignUpForm()
    return render(request, 'upload/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {username}!")
                return redirect('upload:subject_list')  # Добавляем неймспейс
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'upload/login.html', {'form': form})

@login_required
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have successfully logged out.")
    return redirect('upload:login')  # Добавляем неймспейс

@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'upload/subject_list.html', {'subjects': subjects})

@login_required
def subject_detail(request, subject_name):
    subject = get_object_or_404(Subject, name=subject_name)
    assignments = subject.assignments.all()
    # Retrieve grades for the current user
    user = request.user
    user_documents = Document.objects.filter(user=user, assignment__subject=subject)
    grades = {doc.assignment.name: doc.grade for doc in user_documents}

    return render(request, 'upload/subject_detail.html', {
        'subject': subject,
        'assignments': assignments,
        'grades': grades,
    })

def run_tests(assignment, file_path):
    # Define the path to the test file based on assignment
    # Naming convention: {SubjectAbbreviation}{AssignmentNumber}_tests.py
    subject_abbr = assignment.subject.name.upper()  # e.g., 'DSA'

    # Extract the assignment number from assignment name, e.g., 'Homework 6' -> '6'
    match = re.search(r'Homework\s+(\d+)', assignment.name, re.IGNORECASE)
    if match:
        assignment_number = match.group(1)
    else:
        return (0, 0, "Cannot determine assignment number from the assignment name.")

    test_file_name = f"{subject_abbr}{assignment_number}_tests.py"
    test_file_path = os.path.join(os.path.dirname(__file__), 'tests', test_file_name)

    if not os.path.exists(test_file_path):
        return (0, 0, f"Test file '{test_file_name}' not found for this assignment.")

    try:
        # Load the test module
        spec = importlib.util.spec_from_file_location("test_module", test_file_path)
        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)

        # Load the student module
        spec_student = importlib.util.spec_from_file_location("student_code", file_path)
        student_module = importlib.util.module_from_spec(spec_student)
        spec_student.loader.exec_module(student_module)

        # Run the tests
        passed_tests, total_tests, message = test_module.run_tests(student_module)

        return (passed_tests, total_tests, message)

    except Exception as e:
        return (0, 0, f"Failed to run tests: {e}")


@login_required
def assignment_detail(request, subject_name, assignment_id):
    assignment = get_object_or_404(Assignment, subject__name=subject_name, id=assignment_id)
    documents = assignment.documents.filter(user=request.user)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_files = request.FILES.getlist('document')  # Получаем список файлов
            if not uploaded_files:
                messages.error(request, 'No files selected for upload.')
            else:
                for uploaded_file in uploaded_files:
                    # Создаём объект Document для каждого файла
                    document = Document.objects.create(
                        assignment=assignment,
                        user=request.user,
                        document=uploaded_file,
                        description=form.cleaned_data.get('description', '')
                    )

                    # Запускаем тесты на загруженном коде
                    file_path = document.document.path
                    passed_tests, total_tests, message = run_tests(assignment, file_path)

                    # Вычисляем оценку
                    if total_tests > 0:
                        grade = passed_tests  # Предполагается, что каждый тест стоит 1 балл
                    else:
                        grade = 0  # Тесты не найдены, оценка 0

                    # Обновляем объект Document с результатами тестов и оценкой
                    if total_tests == 0:
                        # Тестовый файл не найден
                        document.test_result = f"Failed: {message}"
                        messages.error(request, f'File "{uploaded_file.name}" uploaded but tests could not be run: {message}')
                    elif passed_tests == total_tests:
                        # Все тесты пройдены
                        document.test_result = "Passed: All tests passed successfully."
                        messages.success(request, f'File "{uploaded_file.name}" uploaded and passed all tests!')
                    else:
                        # Некоторые тесты не пройдены
                        document.test_result = f"Failed: {message}"
                        messages.error(request, f'File "{uploaded_file.name}" uploaded but failed some tests: {message}')

                    document.grade = grade
                    document.save()

                return redirect('upload:assignment_detail', subject_name=subject_name, assignment_id=assignment_id)  # Добавляем неймспейс
        else:
            messages.error(request, 'There was an error uploading your file.')
    else:
        form = DocumentForm()

    # Определяем, является ли пользователь учителем
    is_teacher_flag = is_teacher(request.user)

    return render(request, 'upload/assignment_detail.html', {
        'assignment': assignment,
        'documents': documents,
        'form': form,
        'is_teacher': is_teacher_flag,  # Передаём 'is_teacher' в шаблон
    })


@login_required
def delete_document(request, pk):
    document = get_object_or_404(Document, pk=pk, user=request.user)
    if request.method == 'POST':
        document.document.delete()  # Delete file from disk
        document.delete()           # Delete record from database
        messages.success(request, "File successfully deleted.")
        return redirect('upload:assignment_detail', subject_name=document.assignment.subject.name, assignment_id=document.assignment.id)  # Добавляем неймспейс
    return render(request, 'upload/delete_document.html', {'document': document})


@login_required
@user_passes_test(is_teacher)
def upload_test_file(request, subject_abbr, assignment_number):
    subject = get_object_or_404(Subject, name=subject_abbr)
    assignment_name = f"Homework {assignment_number}"
    assignment = get_object_or_404(Assignment, subject=subject, name=assignment_name)

    if request.method == 'POST':
        form = TestFileForm(request.POST, request.FILES)
        if form.is_valid():
            test_file = form.cleaned_data['test_file']
            expected_test_file_name = f"{subject_abbr}{assignment_number}_tests.py"

            if test_file.name != expected_test_file_name:
                messages.error(request, f"Test file must be named '{expected_test_file_name}'.")
            else:
                test_file_path = os.path.join(os.path.dirname(__file__), 'tests', expected_test_file_name)
                # Убедитесь, что директория 'tests' существует
                os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
                with open(test_file_path, 'wb+') as destination:
                    for chunk in test_file.chunks():
                        destination.write(chunk)
                messages.success(request, "Test file uploaded successfully.")
                return redirect('upload:assignment_detail', subject_name=subject_abbr, assignment_id=assignment.id)  # Добавляем неймспейс
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = TestFileForm()

    return render(request, 'upload/upload_test_file.html', {
        'form': form,
        'subject_abbr': subject_abbr,
        'assignment_number': assignment_number,
        'assignment': assignment,
    })
