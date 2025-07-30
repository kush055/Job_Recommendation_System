import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Resume, Recommendation
from accounts.models import Activity
from .utils.ocr_utils import extract_text_from_resume
from .utils.recommender import generate_recommendations
from .forms import ResumeUploadForm


def about_view(request):
    return render(request, 'about.html', {
        'nav_mode': 'about_page'
    })


def home(request):
    return render(request, 'home.html')


@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = form.cleaned_data['file']
            resume = Resume.objects.create(user=request.user, file=resume_file)

            extracted_text = extract_text_from_resume(resume.file.path)
            resume.text_content = extracted_text
            resume.save()

            recommendations, unmatched_resume_skills = generate_recommendations(extracted_text)

            enriched_recommendations = []
            recommendation_titles = []

            for rec in recommendations:
                rec_obj = Recommendation.objects.create(
                    resume=resume,
                    job_title=rec['title'],
                    job_description=rec['description'],
                    match_percent=rec['match_percent']
                )
                enriched_recommendations.append({
                    'title': rec['title'],
                    'description': rec['description'],
                    'match_percent': rec['match_percent'],
                    'matched_skills': rec.get('matched_skills', []),
                    'unmatched_skills': rec.get('unmatched_skills', []),
                    'job_id': rec_obj.id  # Add job ID for apply button
                })
                recommendation_titles.append(rec['title'])

            Activity.objects.create(
                user=request.user,
                action='recommendation',
                description=f"Uploaded resume and received recommendations: {', '.join(recommendation_titles)}",
                resume=resume
            )

            request.session['extra_recommendation_data'] = enriched_recommendations
            request.session['unmatched_resume_skills'] = unmatched_resume_skills

            messages.success(request, "Resume uploaded and recommendations generated!")
            return redirect('resumes:results', resume_id=resume.id)
        else:
            messages.error(request, "There was a problem with your form.")
    else:
        form = ResumeUploadForm()

    return render(request, 'resumes/upload.html', {
        'form': form,
        'nav_mode': 'upload_page'
    })


@login_required
def results_view(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    db_recommendations = resume.recommendations.all().order_by('-match_percent')

    extra_data = request.session.pop('extra_recommendation_data', [])
    unmatched_resume_skills = request.session.pop('unmatched_resume_skills', [])

    enriched = []
    for db_rec in db_recommendations:
        match = next((r for r in extra_data if r['title'] == db_rec.job_title), {})
        enriched.append({
            'title': db_rec.job_title,
            'description': db_rec.job_description,
            'match_percent': db_rec.match_percent,
            'matched_skills': match.get('matched_skills', []),
            'unmatched_skills': match.get('unmatched_skills', []),
            'job_id': db_rec.id  # for Apply Now button
        })

    return render(request, 'resumes/results.html', {
        'resume': resume,
        'recommendations': enriched,
        'unmatched_skills': unmatched_resume_skills,
        'nav_mode': 'upload_page'
    })


@login_required
def history_view(request):
    activities = Activity.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'resumes/history.html', {
        'activities': activities,
        'nav_mode': 'upload_page'
    })


# ✅ New View for "Apply Now"
@login_required
def apply_job(request, job_id):
    recommendation = get_object_or_404(Recommendation, id=job_id)
    Activity.objects.create(
        user=request.user,
        action='applied',
        description=f"Applied for job: {recommendation.job_title}",
        resume=recommendation.resume
    )
    messages.success(request, f"You have successfully applied for '{recommendation.job_title}'!")
    return redirect('resumes:results', resume_id=recommendation.resume.id)
