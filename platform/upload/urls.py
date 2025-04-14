# upload/urls.py

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'upload'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),

    path('delete/<int:pk>/', views.delete_document, name='delete_document'),
    path('upload-test/<str:subject_abbr>/<int:assignment_number>/', views.upload_test_file, name='upload_test_file'),
    path('document/<int:pk>/', views.document_detail, name='document_detail'),
    path('grades-overview/', views.grades_overview, name='grades_overview'),
    path('<str:subject_name>/<int:assignment_id>/code-editor/', views.assignment_code_editor, name='assignment_code_editor'),
    path('', views.subject_list, name='subject_list'),
    path('<str:subject_name>/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('<str:subject_name>/', views.subject_detail, name='subject_detail'),

    # Teacher URLs
    path('teacher/subjects/', views.teacher_subject_list, name='teacher_subject_list'),
    path('teacher/subjects/create/', views.teacher_subject_create, name='teacher_subject_create'),
    path('teacher/subjects/delete/<int:pk>/', views.teacher_subject_delete, name='teacher_subject_delete'),

    path('teacher/subjects/<int:pk>/assignments/', views.teacher_assignment_list, name='teacher_assignment_list'),
    path('teacher/subjects/<int:pk>/assignments/create/', views.teacher_assignment_create, name='teacher_assignment_create'),
    path('teacher/assignments/delete/<int:pk>/', views.teacher_assignment_delete, name='teacher_assignment_delete'),
    path('teacher/assignments/<int:pk>/submissions/', views.teacher_assignment_submissions, name='teacher_assignment_submissions'),
    path('teacher/assignments/<int:assignment_id>/plagiarism/<str:method>/', views.teacher_plagiarism_check, name='teacher_plagiarism_check'),
]
