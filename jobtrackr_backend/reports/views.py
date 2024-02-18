import json

import os
from openai import OpenAI
import requests
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from dashboard.models import Report, Company, NewsItem

RAPIDAPI_KEY = "0a886d1acfmshf7f6f25447d1423p1b3abejsn0ecf3486e01a"
OPENAI_API_KEY = "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"
GOOGLE_API_KEY = "AIzaSyB7_m3xeyd8t1L5PoFtugu596oFl0xModk"
model = "gpt-3.5-turbo"
client = OpenAI(
    api_key=OPENAI_API_KEY
)


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
        context['total_reviews'] = report.total_reviews
        context['overall_rating'] = report.overall_rating
        context['rating_distribution'] = report.rating_distribution
        context['top_reviews'] = report.top_reviews
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
            context['sector'] = context['projects'] = context['website_url'] = context['total_reviews'] = \
            context['overall_rating'] = context['rating_distribution'] = context['top_reviews'] = \
            context['location'] = "Report does not exist"
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
        description_prompt = f"Give me a comprehensive overview of the company {company_name}."
        projects_prompt = f"Tell me about some big projects by the company {company_name} that are relevant to {job_title}."

        if not company_name or not job_title or not location:
            return JsonResponse({"error": "No company name, location or job title provided"}, status=400)

        # Fetch the description and projects from ChatGPT API
        try:
            description_response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": description_prompt
                    }
                ],
            )

            project_response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": projects_prompt
                    }
                ],
            )
            description = description_response.choices[0].message.content.strip()
            projects = project_response.choices[0].message.content.strip()

        except Exception as e:
            return JsonResponse({"error": f"Failed to fetch data from OpenAI: {str(e)}"}, status=500)

        try:
            company_id = get_company_id(company_name)
            company_details = get_company_details(company_id)
            website_url = company_details.get('website', '')
            salary_details = get_salary_info(job_title, location)
            news_details = get_news_info(company_name)
            ratings_reviews_data = get_company_ratings_and_reviews(company_name, location)
            if not ratings_reviews_data:
                return JsonResponse({"error": "Failed to fetch ratings and reviews data."}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data provided."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        if not company_details or not salary_details or not ratings_reviews_data:
            return JsonResponse({"error": "Required company, ratings or salary information is missing"}, status=500)

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
            sector=company_details.get('sector', 'Unknown'),
            website_url=website_url,
            total_reviews=ratings_reviews_data.get('total_reviews'),
            overall_rating=ratings_reviews_data.get('overall_rating', 0.0),
            rating_distribution=ratings_reviews_data.get('rating_distribution'),
            top_reviews=ratings_reviews_data.get('top_reviews'),
        )

        for news in news_details[:3]:  # Limit to top 3 news items
            NewsItem.objects.create(
                report=report,
                title=news.get('title'),
                snippet=news.get('snippet'),
                url=news.get('newsUrl')
            )

        return JsonResponse(
            {'message': 'Report created successfully', 'id': report.id})
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


def get_company_ratings_and_reviews(company_name, location):
    if not company_name or not location:
        return JsonResponse({"error": "Missing required parameters: company_name or location"}, status=400)

    # Find the place ID for the company
    search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    search_params = {
        "query": f"{company_name} near {location}",
        "key": GOOGLE_API_KEY,
    }
    search_resp = requests.get(search_url, params=search_params)
    search_results = search_resp.json()

    if search_resp.status_code != 200 or not search_results.get('results'):
        return JsonResponse({"error": "Failed to fetch company ID or company not found"},
                            status=search_resp.status_code)

    place_id = search_results['results'][0].get('place_id')

    # Use the place ID to get details
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    details_params = {
        "place_id": place_id,
        "fields": "rating,reviews,user_ratings_total",
        "key": GOOGLE_API_KEY,
    }
    details_resp = requests.get(details_url, params=details_params)
    details = details_resp.json()

    if details_resp.status_code != 200 or 'result' not in details:
        return JsonResponse({"error": "Failed to fetch company details"}, status=details_resp.status_code)

    company_details = details['result']
    overall_rating = company_details.get("rating", "No rating available")
    total_reviews = company_details.get("user_ratings_total", 0)
    reviews = company_details.get("reviews", [])

    # Calculate rating distribution from all reviews
    rating_distribution = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
    for review in reviews:
        rating = str(int(review.get("rating", 0)))  # Ensure the rating is an integer then convert to string
        if rating in rating_distribution:
            rating_distribution[rating] += 1

    # Extract top 3 reviews for detailed information
    top_reviews = [{
        "author_name": review.get("author_name"),
        "rating": review.get("rating"),
        "text": review.get("text"),
        "time": review.get("time")
    } for review in reviews][:3]

    response_data = {
        "overall_rating": overall_rating,
        "total_reviews": total_reviews,
        "top_reviews": top_reviews,
        "rating_distribution": rating_distribution,
    }

    return response_data



