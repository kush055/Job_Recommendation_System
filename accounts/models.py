from django.db import models
from django.contrib.auth.models import User
from resumes.models import Resume

# ----------------------------
# User Profile Model
# ----------------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# ----------------------------
# User Settings Model
# ----------------------------
class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    receive_newsletter = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)
    language_preference = models.CharField(max_length=10, default='en')

    def __str__(self):
        return f"{self.user.username}'s Settings"


# ----------------------------
# Unified Activity Log Model
# ----------------------------
class Activity(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('register', 'Register'),
        ('recommendation', 'Recommendation'),
        ('upload_resume', 'Uploaded Resume'),
        ('apply_job', 'Applied to Job'),
        # Add more as needed
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)  # ✅ Use this instead of "details"
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
