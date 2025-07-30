from django.core.management.base import BaseCommand
from jobs.models import Job

class Command(BaseCommand):
    help = 'Seed the database with sample job listings'

    def handle(self, *args, **kwargs):
        jobs = [
            {
                'title': 'Backend Developer',
                'company_name': 'Infosys',
                'location': 'Bengaluru',
                'description': 'Develop REST APIs using Django and PostgreSQL.',
                'apply_link': 'https://infosys.com/careers/backend',
            },
            {
                'title': 'Data Analyst Intern',
                'company_name': 'TCS',
                'location': 'Mumbai',
                'description': 'Perform data cleaning and analysis using Python, SQL, and Excel.',
                'apply_link': 'https://tcs.com/careers/data-analyst',
            },
            {
                'title': 'Machine Learning Engineer',
                'company_name': 'Google',
                'location': 'Hyderabad',
                'description': 'Build and deploy ML models using TensorFlow and scikit-learn.',
                'apply_link': 'https://google.com/careers/ml-engineer',
            },
        ]

        for job in jobs:
            Job.objects.get_or_create(**job)

        self.stdout.write(self.style.SUCCESS("Sample jobs added successfully."))
