from django.urls import path
from . import views
from .views import about_view

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='list'),
    path('about/', about_view, name='about'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('search/', views.job_search, name='job_search'),
    path('filter/', views.job_filter, name='job_filter'),
    path('apply/<int:job_id>/', views.job_apply, name='job_apply'),
    path('<int:job_id>/apply/', views.job_apply, name='apply'),
    path('search/', views.job_search, name='job_search'),
    path('filter/', views.job_filter, name='job_filter'),

]
