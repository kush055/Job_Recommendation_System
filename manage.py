#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_recommendation.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
# # The Recommendation model links resumes to job postings, storing job title, description, match percentage, and creation timestamp.
# # It includes methods to return string representations of the models. 
# # The UploadedResume model is used to track resumes uploaded by users, linking them to the User model.
# # The manage.py script is the entry point for Django administrative tasks, setting up the environment and executing commands.
# # It ensures that the Django settings module is set and handles import errors gracefully.
# # This script is essential for running the Django application, managing migrations, and performing other administrative tasks.
# # The code is structured to be run as a standalone script, making it easy to manage the Django project from the command line.
# # The models are designed to work with Django's ORM, allowing for easy database interactions and migrations.
# # The UploadedResume model is specifically for tracking resumes uploaded by users, while the Resume model is for storing processed resumes with OCR-extracted text.
# # The Recommendation model is used to store job recommendations based on the resumes, allowing for easy retrieval and analysis.   
# # The manage.py script is a standard part of Django projects, providing a command-line interface for various administrative tasks.
# # It is essential for running the Django application, managing migrations, and performing other administrative tasks.
# # The code is structured to be run as a standalone script, making it easy to manage the Django project from the command line.
# # The models are designed to work with Django's ORM, allowing for easy database interactions and migrations.
# # The UploadedResume model is specifically for tracking resumes uploaded by users, while the Resume model is for storing processed resumes with OCR-extracted text.
# # The Recommendation model is used to store job recommendations based on the resumes, allowing for easy retrieval and analysis.
# # The manage.py script is a standard part of Django projects, providing a command-line interface for various administrative tasks.
