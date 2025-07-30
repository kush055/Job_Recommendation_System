from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Make sure this refers to job_recommendation/views.py

urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom views
    path('', views.home_view, name='home'),              # Home page
    path('about/', views.about_view, name='about'),      # About Us page

    # App URLs
    path('accounts/', include('accounts.urls')),          # Login, Register, Edit Profile, History
    path('resumes/', include('resumes.urls')),            # Resume upload & processing
    path('jobs/', include('jobs.urls')),                  # Job listings
]

# Media file handling in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Static files handling in development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# This code sets up the URL routing for the Django project, including admin, custom views, and app-specific URLs.
    