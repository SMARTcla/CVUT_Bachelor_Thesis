# upload/views.py

import importlib.util
import os
import re 
import random
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import TestFileForm, DocumentForm, SignUpForm, SubjectForm, AssignmentForm
from .models import Document, Subject, Assignment
from django.core.files.base import ContentFile
from django.contrib import messages

def is_teacher(user):
    return user.is_superuser or user.groups.filter(name='Teachers').exists()

@login_required
@user_passes_test(is_teacher)
def teacher_subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'upload/teacher/subject_list.html', {
        'subjects': subjects
    })

@login_required
@user_passes_test(is_teacher)
def teacher_subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New subject created successfully!")
            return redirect('upload:teacher_subject_list')
    else:
        form = SubjectForm()

    return render(request, 'upload/teacher/subject_create.html', {
        'form': form
    })

login_required
@user_passes_test(is_teacher)
def teacher_subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, "Subject deleted successfully!")
        return redirect('upload:teacher_subject_list')

    return render(request, 'upload/teacher/subject_delete.html', {
        'subject': subject
    })

@login_required
@user_passes_test(is_teacher)
def teacher_assignment_list(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    assignments = subject.assignments.all()
    return render(request, 'upload/teacher/assignment_list.html', {
        'subject': subject,
        'assignments': assignments
    })

@login_required
@user_passes_test(is_teacher)
def teacher_assignment_create(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.subject = subject
            assignment.save()
            messages.success(request, "Assignment created successfully!")
            return redirect('upload:teacher_assignment_list', pk=subject.pk)
    else:
        form = AssignmentForm()

    return render(request, 'upload/teacher/assignment_create.html', {
        'form': form,
        'subject': subject
    })

@login_required
@user_passes_test(is_teacher)
def teacher_assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    subject = assignment.subject
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, "Assignment deleted successfully!")
        return redirect('upload:teacher_assignment_list', pk=subject.pk)

    return render(request, 'upload/teacher/assignment_delete.html', {
        'assignment': assignment
    })


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('upload:subject_list')
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

    is_teacher_flag = request.user.is_superuser or request.user.groups.filter(name='Teachers').exists()

    return render(request, 'upload/subject_list.html', {
        'subjects': subjects,
        'is_teacher_flag': is_teacher_flag
    })

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
    subject_abbr = assignment.subject.name.upper()
    match = re.search(r'Homework\s+(\d+)', assignment.name, re.IGNORECASE)
    if match:
        assignment_number = match.group(1)
    else:
        return (0, 0, "Cannot determine assignment number from the assignment name.")
    
    test_file_name = f"{subject_abbr}{assignment_number}_tests.py"
    test_file_path = os.path.join(os.path.dirname(__file__), 'tests', test_file_name)

    if not os.path.exists(test_file_path):
        return (0, 0, f"Test file '{test_file_name}' not found for this assignment.")
    coderunner_url = "http://test-runner:8003/run-tests"
    params = {
        "file_path": file_path
    }
    try:
        response = requests.get(coderunner_url, params=params)
        if response.status_code != 200:
            return (0, 0, f"Test runner returned error: {response.status_code}")
        data = response.json()
        passed_tests = data.get("passed_tests", 0)
        total_tests = data.get("total_tests", 0)
        message = data.get("message", "")
        return (passed_tests, total_tests, message)
    except Exception as e:
        return (0, 0, f"Exception during contacting test runner: {str(e)}")

@login_required
def assignment_detail(request, subject_name, assignment_id):
    assignment = get_object_or_404(Assignment, subject__name=subject_name, id=assignment_id)

    user_uploads_count = Document.objects.filter(assignment=assignment, user=request.user).count()
    if user_uploads_count >= assignment.max_uploads:
        messages.error(request, f"You have reached the upload limit ({assignment.max_uploads}). You cannot upload more files.")
        return render(request, 'upload/assignment_detail.html', {
            'assignment': assignment,
            'latest_document': None,
            'form': None,
            'is_teacher': is_teacher(request.user),
        })

    documents = Document.objects.filter(user=request.user, assignment=assignment).order_by('-uploaded_at')
    latest_document = documents.first()

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_files = request.FILES.getlist('document')
            if not uploaded_files:
                messages.error(request, 'No files selected for upload.')
            else:
                for uploaded_file in uploaded_files:
                    doc = Document.objects.create(
                        assignment=assignment,
                        user=request.user,
                        document=uploaded_file,
                        description=form.cleaned_data.get('description', '')
                    )
                    file_path = doc.document.path
                    passed_tests, total_tests, message = run_tests(assignment, file_path)

                    if total_tests > 0:
                        fraction_passed = passed_tests / total_tests
                        grade = int(fraction_passed * assignment.max_points)
                    else:
                        grade = 0

                    if total_tests == 0:
                        doc.test_result = f"Failed: {message}"
                        messages.error(request, f'File "{uploaded_file.name}" uploaded but tests could not be run: {message}')
                    elif passed_tests == total_tests:
                        doc.test_result = "Passed: All tests passed successfully."
                        messages.success(request, f'File "{uploaded_file.name}" uploaded and passed all tests!')
                    else:
                        doc.test_result = f"Failed: {message}"
                        messages.error(request, f'File "{uploaded_file.name}" uploaded but failed some tests: {message}')

                    doc.grade = grade
                    doc.save()

                return redirect('upload:assignment_detail', subject_name=subject_name, assignment_id=assignment_id)
        else:
            messages.error(request, 'There was an error uploading your file.')
    else:
        form = DocumentForm()

    return render(request, 'upload/assignment_detail.html', {
        'assignment': assignment,
        'latest_document': latest_document,
        'user_uploads_count': user_uploads_count,
        'form': form,
        'is_teacher': is_teacher(request.user),
    })


@login_required
def delete_document(request, pk):
    document = get_object_or_404(Document, pk=pk, user=request.user)
    if request.method == 'POST':
        document.document.delete()
        document.delete()
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


@login_required
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if document.user == request.user or is_teacher(request.user):
        try:
            with open(document.document.path, 'r') as f:
                code_content = f.read()
        except Exception as e:
            code_content = f"No code found: {e}"
        
        return render(request, 'upload/document_detail.html', {
            'document': document,
            'code_content': code_content,
        })
    else:
        from django.http import Http404
        raise Http404("No Document matches the given query.")


@login_required
def grades_overview(request):
    user = request.user
    subjects = Subject.objects.all().order_by('name')
    subject_data = []

    for subj in subjects:
        assignment_rows = []
        total_subject_max = 0
        total_subject_user = 0
        for asg in subj.assignments.all().order_by('deadline'):
            docs = asg.documents.filter(user=user)
            best_doc = docs.order_by('-grade').first()
            user_grade = 0
            if best_doc:
                user_grade = best_doc.grade

            assignment_rows.append({
                'assignment': asg,
                'deadline': asg.deadline,
                'max_points': asg.max_points,
                'user_grade': user_grade,
            })
            total_subject_max += asg.max_points
            total_subject_user += user_grade

        subject_data.append({
            'subject': subj,
            'assignments': assignment_rows,
            'subject_max': total_subject_max,
            'subject_user': total_subject_user,
        })

    return render(request, 'upload/grades_overview.html', {
        'subject_data': subject_data,
    })

@login_required
def assignment_code_editor(request, subject_name, assignment_id):
    assignment = get_object_or_404(Assignment, subject__name=subject_name, id=assignment_id)

    documents = Document.objects.filter(assignment=assignment, user=request.user).order_by('-uploaded_at')
    user_uploads_count = documents.count()
    if user_uploads_count >= assignment.max_uploads:
        messages.error(request, "Upload limit reached. Cannot open code editor.")
        return redirect('upload:assignment_detail', subject_name=subject_name, assignment_id=assignment_id)

    latest_doc = documents.first()
    initial_code = ""
    if latest_doc:
        try:
            with open(latest_doc.document.path, 'r') as f:
                initial_code = f.read().rstrip('\n')
        except Exception as e:
            initial_code = f"# Cannot read last file: {e}"

    if request.method == "POST":
        code_from_editor = request.POST.get("editor_code", "")

        random_part = str(random.randrange(1000,9999))
        filename = f"calculate_{random_part}.py"

        content_file = ContentFile(code_from_editor.encode('utf-8'), name=filename)

        doc = Document.objects.create(
            assignment=assignment,
            user=request.user,
            document=content_file,
        )

        file_path = doc.document.path
        passed_tests, total_tests, message = run_tests(assignment, file_path)

        if total_tests > 0:
            fraction_passed = passed_tests / total_tests
            grade = int(fraction_passed * assignment.max_points)
        else:
            grade = 0

        if total_tests == 0:
            doc.test_result = f"Failed: {message}"
            messages.error(request, f'Your code was uploaded but tests could not be run: {message}')
        elif passed_tests == total_tests:
            doc.test_result = "Passed: All tests passed successfully."
            messages.success(request, 'Your code was uploaded and passed all tests!')
        else:
            doc.test_result = f"Failed: {message}"
            messages.error(request, f'Your code was uploaded but failed some tests: {message}')

        doc.grade = grade
        doc.save()

        return redirect('upload:assignment_detail', subject_name=subject_name, assignment_id=assignment_id)

    return render(request, 'upload/assignment_code_editor.html', {
        'assignment': assignment,
        'initial_code': initial_code,
    })



@login_required
@user_passes_test(is_teacher)
def teacher_assignment_submissions(request, pk):
    """
    Displays a list of all submissions for a given assignment.
    """
    assignment = get_object_or_404(Assignment, pk=pk)
    submissions = assignment.documents.all().order_by('-uploaded_at')
    
    return render(request, 'upload/teacher/assignment_submissions.html', {
        'assignment': assignment,
        'submissions': submissions,
    })


@login_required
@user_passes_test(is_teacher)
def teacher_plagiarism_check(request, assignment_id, method):    
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    
    docs = Document.objects.filter(assignment=assignment).order_by('-uploaded_at')
    submissions = {}
    for doc in docs:
        if doc.user.username not in submissions:
            submissions[doc.user.username] = doc

    usernames = list(submissions.keys())
    n = len(usernames)
    pairwise_results = []
    for i in range(n):
        for j in range(i + 1, n):
            user1 = usernames[i]
            user2 = usernames[j]
            try:
                with open(submissions[user1].document.path, 'r') as f:
                    code1 = f.read()
            except Exception:
                code1 = ""
            try:
                with open(submissions[user2].document.path, 'r') as f:
                    code2 = f.read()
            except Exception:
                code2 = ""
            base_url = "http://antiplagiat:8004/check-plagiarism"
            params = {
                "file1": submissions[user1].document.path,
                "file2": submissions[user2].document.path,
                "method": method
            }
            response = requests.get(base_url, params=params)
            pairwise_results.append((user1, user2, int(round(float(response.text[:len(response.text)])))))
    max_scores = {}
    for user in usernames:
        max_score = 0
        for (u1, u2, score) in pairwise_results:
            if u1 == user or u2 == user:
                if score > max_score:
                    max_score = score
        max_scores[user] = max_score

    return render(request, 'upload/teacher/plagiarism_results.html', {
        'assignment': assignment,
        'pairwise_results': pairwise_results,
        'max_scores': max_scores,
        'method': method,
    })