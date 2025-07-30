from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Activity History
    path('history/', views.user_history, name='history'),

    # Profile
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]