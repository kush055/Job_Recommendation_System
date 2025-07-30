from django.db import models
from django.contrib.auth.models import User
from resumes.models import Resume

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    skills = models.CharField(max_length=300)
    experience_required = models.CharField(max_length=100)
    apply_link = models.URLField(blank=True, null=True)  # Optional external link
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"


class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} applied to {self.job.title}"

    class Meta:
        unique_together = ('user', 'job')  # prevent duplicate applications
        ordering = ['-applied_at']
