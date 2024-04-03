from django.urls import path
from . import views

app_name = 'interviews'
urlpatterns = [
    path('start_interview/<int:application_id>/', views.start_interview, name='start_interview'),
    path('get_interviews/', views.get_interviews, name='list_interviews'),
    path('get_interview_questions/<int:interview_id>/', views.get_interview_questions, name='get_interview_questions'),
    path('<int:interview_id>/delete/', views.delete_interview, name='delete_application'),
    path('upload_audio_answers/', views.upload_audio, name='upload_audio'),
    path('get_interview_feedback/<int:interview_id>/', views.get_interview_feedback, name='interview_feedback'),
    path('get_job_details/<int:interview_id>/', views.get_job_details, name='get_job_details'),
]
