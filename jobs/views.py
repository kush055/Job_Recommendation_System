from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Job, JobApplication
from resumes.models import Resume
from accounts.models import Activity  # For logging activity

def about_view(request):
    return render(request, 'about.html')

def job_list(request):
    jobs = Job.objects.all().order_by('-posted_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    has_applied = False
    if request.user.is_authenticated:
        has_applied = JobApplication.objects.filter(user=request.user, job=job).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'has_applied': has_applied})

def job_search(request):
    query = request.GET.get('q', '').strip()
    jobs = Job.objects.none()
    if query:
        jobs = Job.objects.filter(title__icontains=query) | Job.objects.filter(description__icontains=query)
    return render(request, 'jobs/job_search.html', {'jobs': jobs, 'query': query})

def job_filter(request):
    location = request.GET.get('location', '').strip()
    skills = request.GET.get('skills', '').strip()
    experience = request.GET.get('experience', '').strip()

    jobs = Job.objects.all()
    if location:
        jobs = jobs.filter(location__icontains=location)
    if skills:
        jobs = jobs.filter(skills__icontains=skills)
    if experience:
        jobs = jobs.filter(experience_required__icontains=experience)

    return render(request, 'jobs/job_filter.html', {
        'jobs': jobs,
        'location': location,
        'skills': skills,
        'experience': experience
    })

@login_required
def job_apply(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    resumes = Resume.objects.filter(user=request.user)

    if JobApplication.objects.filter(user=request.user, job=job).exists():
        messages.info(request, "You have already applied for this job.")
        return redirect('jobs:job_detail', job_id=job.id)

    if request.method == 'POST':
        resume_id = request.POST.get('resume_id')
        cover_letter = request.POST.get('cover_letter', '')

        if not resume_id:
            messages.error(request, "Please select a resume to apply with.")
            return redirect('jobs:job_apply', job_id=job.id)

        resume = get_object_or_404(Resume, id=resume_id, user=request.user)

        application = JobApplication.objects.create(
            user=request.user,
            job=job,
            resume=resume,
            cover_letter=cover_letter
        )

        # Activity Log
        Activity.objects.create(
            user=request.user,
            action=f"Applied for job: {job.title} at {job.company}",
            resume=resume
        )

        messages.success(request, f"Successfully applied to {job.title}.")
        return redirect('jobs:job_detail', job_id=job.id)

    return render(request, 'jobs/job_apply.html', {
        'job': job,
        'resumes': resumes
    })
