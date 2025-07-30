from django.contrib import admin
from .models import Resume, Recommendation

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('user__username',)

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('id', 'resume', 'job_title', 'match_percent', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('job_title', 'resume__user__username')
# This code registers the Resume and Recommendation models with the Django admin site,
# allowing administrators to manage resumes and job recommendations through the admin interface.