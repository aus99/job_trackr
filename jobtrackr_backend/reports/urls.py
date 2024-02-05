from django.urls import path
from . import views

app_name = 'reports'
urlpatterns = [
    path('create_report/', views.create_report, name='create_report'),
    path('get_reports/', views.get_reports, name='get_reports'),
    path('<int:report_id>/', views.view_report, name='view_report'),
    path('<int:report_id>/delete/', views.delete_report, name='delete_report')
]