import json

from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.utils import json


from .models import Application, Job, Company


def view_application_list(request):
    applications = Application.objects.all()
    application_array = []
    for application in applications:
        context = {'id': application.id,
                   'job_title': application.job.title,
                   'company_name': application.job.company.name,
                   'status': application.status,
                   'location': application.job.location,
                   'description':application.job.description,
                   }
        application_array.append(context)

    return JsonResponse(application_array, safe=False)


@api_view(['POST'])
@permission_classes([AllowAny])
def new_application(request):
    if request.method == 'POST':
        post_data = json.loads(request.body)
        title = post_data['job_title']
        company_name = post_data['company_name']
        location = post_data['job_location']
        status = post_data['application_status']
        description = post_data['job_description']

        company, created = Company.objects.get_or_create(name=company_name)
        job = Job.objects.create(title=title, description=description, location=location, company=company)
        application = Application.objects.create(job=job, status=status)
        return JsonResponse(
            {'message': 'Application created successfully', 'id': application.id})  # Send back some identifier
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_application(request, application_id):
    if request.method == 'DELETE':

        application = get_object_or_404(Application, pk=application_id)
        job = application.job


        application.delete()

        # Check if the job is not related to other applications before deleting
        if not Application.objects.filter(job=job).exists():

            job.delete()

        return JsonResponse({'message': 'Application and    its corresponding job were deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@api_view(['PUT'])
@permission_classes([AllowAny])
def update_application(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    job = application.job

    if request.method == 'PUT':
        post_data = json.loads(request.body.decode('utf-8'))

        # Update or get company details
        company_name = post_data.get('company_name')
        company, created = Company.objects.get_or_create(name=company_name)

        # Update job details

        job.title = post_data.get('job_title', job.title)
        job.company = company
        job.location = post_data.get('job_location', job.location)
        job.description = post_data.get('job_description', job.description)
        job.save()

        # Update application details
        application.status = post_data.get('application_status', application.status)
        application.save()

        return JsonResponse({'message': 'Application updated successfully', 'id': application.id}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
