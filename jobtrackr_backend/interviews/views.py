import os
import tempfile
from io import BytesIO

import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from openai import OpenAI
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from dashboard.models import Application, Interview, InterviewQuestion, InterviewAnswer

OPENAI_API_KEY = "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"
model = "gpt-3.5-turbo"
client = OpenAI(
    api_key=OPENAI_API_KEY
)


@permission_classes([AllowAny])
@api_view(['POST'])
def start_interview(request, application_id):
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    interview = Interview.objects.create(application=application)
    questions = generate_interview_questions(application.job.description)

    for question_text in questions:
        if question_text.strip():  # Check if question_text is not empty
            InterviewQuestion.objects.create(
                interview=interview,
                question_text=question_text
            )

    return JsonResponse(
        {'message': 'Interview questions created successfully', 'id': interview.id}
    )


def get_interviews(request):
    interviews = Interview.objects.all()
    interview_array = []
    for interview in interviews:
        context = {'id': interview.id,
                   'application_id': interview.application.id,
                   'job_title': interview.application.job.title,
                   'company_name': interview.application.job.company.name,
                   'created_at': interview.created_at,
                   'answered': interview.answered,
                   }
        interview_array.append(context)

    return JsonResponse(interview_array, safe=False)


def get_interview_questions(request, interview_id):
    interview = Interview.objects.get(id=interview_id)
    interview_question_list = InterviewQuestion.objects.filter(interview=interview)
    questions_array = []
    for question in interview_question_list:
        context = {'id': question.id,
                   'question_text': question.question_text,
                   }
        questions_array.append(context)
    return JsonResponse(questions_array, safe=False)


def get_job_details(request, interview_id):
    interview = Interview.objects.get(id=interview_id)
    job_title = interview.application.job.title
    company = interview.application.job.company.name
    context = {'job_title': job_title,
               'company': company,
               }
    return JsonResponse(context, safe=False)


def get_interview_feedback(request, interview_id):
    interview = Interview.objects.get(id=interview_id)
    interview_question_list = InterviewQuestion.objects.filter(interview=interview)
    results_array = []
    for question in interview_question_list:
        answer = InterviewAnswer.objects.get(question=question)
        context = {'question_id': question.id,
                   'answer_id': answer.id,
                   'question_text': question.question_text,
                   'answer_text': answer.answer_text,
                   'feedback': answer.feedback
                   }
        results_array.append(context)
    return JsonResponse(results_array, safe=False)


def generate_interview_questions(job_description):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"Create three interview questions based on this job description: {job_description}"
            }
        ],
        temperature=0.5,
        max_tokens=150,
        top_p=1
    )
    questions = response.choices[0].message.content.strip().split('\n')
    return questions


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_interview(request, interview_id):
    if request.method == 'DELETE':
        interview = get_object_or_404(Interview, pk=interview_id)

        questions_to_delete = InterviewQuestion.objects.filter(interview=interview)
        for question in questions_to_delete:
            answers_to_delete = InterviewAnswer.objects.filter(question=question)
            for answer in answers_to_delete:
                answer.delete()
            question.delete()
        interview.delete()

        return JsonResponse({'message': 'Interview was deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@api_view(['POST'])
@permission_classes([AllowAny])
def upload_audio(request):
    if request.method == 'POST':
        file_keys = [key for key in request.FILES if key.startswith('audioBlob_')]
        question_ids = [request.POST.get(f'question_id_{key.split("_")[1]}') for key in file_keys]

        for audio_file_key, question_id in zip(file_keys, question_ids):
            audio_file = request.FILES[audio_file_key]
            audio_bytes = BytesIO(audio_file.read())

            # Convert the audio file directly using a utility function
            text_transcript = convert_audio_to_text(audio_bytes)
            question = InterviewQuestion.objects.get(id=question_id)
            interview = question.interview
            job_description = interview.application.job.description

            # Use the utility function to get feedback from OpenAI's API
            prompt = create_prompt(text_transcript, job_description, question.question_text)
            feedback = get_feedback(prompt)

            # Create InterviewAnswer instance
            InterviewAnswer.objects.create(
                    question=question,
                    answer_text=text_transcript,
                    feedback=feedback
                )

            # Mark the interview as answered
            interview.answered = True
            interview.save()

        return JsonResponse({'message': 'Answers uploaded successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def convert_audio_to_text(audio_bytes):
    file_extension = 'wav'

    # Create a temporary file with the correct extension
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as tmp_file:
        tmp_file_name = tmp_file.name
        audio_bytes.seek(0)  # Ensure you're reading from the start of BytesIO object
        tmp_file.write(audio_bytes.read())


    try:
        with open(tmp_file_name, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
            )
            text_transcription = transcription.text
    finally:
        os.remove(tmp_file_name)

    return text_transcription


def get_feedback(prompt):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
        max_tokens=1024,
    )
    feedback = response.choices[0].message.content.strip()
    return feedback


@staticmethod
def create_prompt(transcript, job_description, question):
    return (
            f"Given the job description: {job_description}\n"
            f"and the interview question: {question}\n"
            f"here is the candidate's response: {transcript}\n\n"
            f"Please provide a critical analysis/feedback of the response in terms of its relevance to the job "
            f"description and the question asked. Also include suggestions for improvement where appropriate"
        )
