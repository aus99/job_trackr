from django.urls import path
from .views import new_application, view_application_list, delete_application, update_application

app_name = 'dashboard'
urlpatterns = [
    path('new_application/', new_application, name='new_application'),
    path('list_applications/', view_application_list, name='view_application_list'),
    path('<int:application_id>/delete/', delete_application, name='delete_application'),
    path('<int:application_id>/update/', update_application, name='update_application')
]
