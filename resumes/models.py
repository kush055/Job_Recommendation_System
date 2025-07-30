from django.db import models
from django.contrib.auth.models import User

class UploadedResume(models.Model):
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_resumes')

    def __str__(self):
        return f"{self.user.username}'s Resume ({self.uploaded_at.strftime('%Y-%m-%d')})"


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    text_content = models.TextField(blank=True, null=True)  # OCR-extracted text
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Resume ({self.uploaded_at.strftime('%Y-%m-%d')})"


class Recommendation(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='recommendations')
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    match_percent = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_title} - {self.match_percent}% Match"


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resume_activities')  # 👈 Fixed here
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)  # e.g., 'Uploaded Resume', 'Generated Recommendations'
    recommendations = models.TextField(blank=True, null=True)  # Comma-separated job titles
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"
