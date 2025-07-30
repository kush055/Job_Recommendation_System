from django.urls import path
from . import views
from .views import about_view

# This code defines the URL patterns for the resumes app, mapping the about view to a specific URL.

app_name = 'resumes'

urlpatterns = [
    path('upload/', views.upload_resume, name='upload'),
    path('results/<int:resume_id>/', views.results_view, name='results'),
    path('about/', about_view, name='about'),
    path('history/', views.history_view, name='history'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
]

# This code defines the URL patterns for the resumes app, mapping the upload and results views to specific URLs.
# It uses Django's path function to create routes for uploading resumes and viewing results.