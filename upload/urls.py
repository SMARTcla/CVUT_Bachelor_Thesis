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

    path('', views.subject_list, name='subject_list'),
    path('<str:subject_name>/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('<str:subject_name>/', views.subject_detail, name='subject_detail'),
]
