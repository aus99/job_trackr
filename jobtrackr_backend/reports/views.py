import json

import requests
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from dashboard.models import Report, Company, NewsItem

RAPIDAPI_KEY = "0a886d1acfmshf7f6f25447d1423p1b3abejsn0ecf3486e01a"


def get_reports(request):
    reports = Report.objects.all()
    report_array = []
    for report in reports:
        context = {'id': report.id,
                   'job_title': report.job_title,
                   'company_name': report.company.name,
                   'location': report.location,
                   }
        report_array.append(context)

    return JsonResponse(report_array, safe=False)


def view_report(request, report_id):
    context = {}
    try:
        report = Report.objects.get(id=report_id)
        context['report_id'] = report.id
        context['description'] = report.description
        context['job_title'] = report.job_title
        context['company_name'] = report.company.name
        context['location'] = report.location
        context['logo'] = report.logo
        context['min_salary'] = report.min_salary
        context['max_salary'] = report.max_salary
        context['median_salary'] = report.median_salary
        context['salary_currency'] = report.salary_currency
        context['sector'] = report.sector
        context['projects'] = report.projects
        context['website_url'] = report.website_url
        news_query_list = NewsItem.objects.filter(report=report)
        context['news_list'] = []
        for news in news_query_list:
            news_dict = {}
            news_dict['id'] = news.id
            news_dict['title'] = news.title
            news_dict['snippet'] = news.snippet
            news_dict['url'] = news.url
            context['news_list'].append(news_dict)
    except Report.DoesNotExist:
        context['report_id'] = context['job_title'] = context['company_name'] = context['logo'] = \
            context['min_salary'] = context['max_salary'] = context['median_salary'] = context['salary_currency'] = \
            context['revenue'] = context['sector'] = context['location'] = "Report does not exist"
    return JsonResponse(context)


@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic
def create_report(request):
    if request.method == 'POST':
        post_data = json.loads(request.body)
        company_name = post_data['company_name']
        job_title = post_data['job_title']
        location = post_data['location']

        if not company_name or not job_title or not location:
            return JsonResponse({"error": "No company name, location or job title provided"}, status=400)

        # Fetch the description and projects from ChatGPT API
        chatgpt_headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "chatgpt-openai1.p.rapidapi.com"
        }
        description_payload = {"query": f"Give me a comprehensive overview of the company {company_name}"}
        projects_payload = {
            "query": f"Tell me about some big projects by the company {company_name} that are relevant to {job_title}"}

        description_response = requests.post("https://chatgpt-openai1.p.rapidapi.com/ask", json=description_payload,
                                             headers=chatgpt_headers)
        projects_response = requests.post("https://chatgpt-openai1.p.rapidapi.com/ask", json=projects_payload,
                                          headers=chatgpt_headers)

        description = description_response.json()['response'] if description_response.status_code == 200 else ""
        projects = projects_response.json()['response'] if projects_response.status_code == 200 else ""

        try:
            company_id = get_company_id(company_name)
            company_details = get_company_details(company_id)
            website_url = company_details.get('website', '')
            salary_details = get_salary_info(job_title, location)
            news_details = get_news_info(company_name)

        except Exception as e:
            print(f"Error fetching external API data: {str(e)}")
            return JsonResponse({"error": "Failed to fetch data from external APIs"}, status=500)

        if not company_details or not salary_details:
            return JsonResponse({"error": "Required company or salary information is missing"}, status=500)

        company, created = Company.objects.get_or_create(name=company_name)
        report = Report.objects.create(
            company=company,
            job_title=job_title,
            location=location,
            logo=company_details.get('logo'),
            description=description,
            projects=projects,
            min_salary=salary_details.get('min_salary'),
            max_salary=salary_details.get('max_salary'),
            median_salary=salary_details.get('median_salary'),
            salary_currency=salary_details.get('salary_currency'),
            sector=company_details.get('sector'),
            website_url=website_url,
        )

        for news in news_details[:3]:  # Limit to top 3 news items
            NewsItem.objects.create(
                report=report,
                title=news.get('title'),
                snippet=news.get('snippet'),
                url=news.get('newsUrl')
            )

        return JsonResponse(
            {'message': 'Report created successfully', 'id': report.id})  # Send back some identifier
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_report(request, report_id):
    if request.method == 'DELETE':
        report = get_object_or_404(Report, pk=report_id)

        news_to_delete = NewsItem.objects.filter(report=report)
        for news in news_to_delete:
            news.delete()
        report.delete()

        return JsonResponse({'message': 'Report was deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_salary_info(job_title, location):
    url = "https://job-salary-data.p.rapidapi.com/job-salary"
    querystring = {"job_title": job_title, "location": location, "radius": "200"}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "job-salary-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        salary_data = response.json().get('data', [])
        if salary_data:
            salary = salary_data[0]
            return {
                "min_salary": salary.get("min_salary"),
                "max_salary": salary.get("max_salary"),
                "median_salary": salary.get("median_salary"),
                "salary_currency": salary.get("salary_currency")
            }
        return None


def get_company_id(company_name):
    search_url = "https://glassdoor.p.rapidapi.com/companies/search"
    search_headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "glassdoor.p.rapidapi.com"
    }
    search_params = {"company_name": company_name}
    search_response = requests.get(search_url, headers=search_headers, params=search_params)

    if search_response.status_code != 200:
        return JsonResponse({"error": "Error fetching company information"}, status=500)

    # Assuming the first result is the most relevant
    company_id = search_response.json()['hits'][0]['id']
    return company_id


def get_company_details(company_id):
    search_headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "glassdoor.p.rapidapi.com"
    }
    details_url = f"https://glassdoor.p.rapidapi.com/company/{company_id}"
    details_response = requests.get(details_url, headers=search_headers)

    if details_response.status_code != 200:
        return JsonResponse({"error": "Error fetching company details"}, status=500)

    return details_response.json()


def get_news_info(company_name):
    url = "https://google-news13.p.rapidapi.com/search"
    querystring = {"keyword": company_name, "lr": "en-US"}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "google-news13.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        news_data = response.json().get('items', [])
        top_news = news_data[:3]  # Get top 3 news items
        news_info = [{
            "title": news.get("title"),
            "snippet": news.get("snippet"),
            "newsUrl": news.get("newsUrl")
        } for news in top_news]
        return news_info
    return None



