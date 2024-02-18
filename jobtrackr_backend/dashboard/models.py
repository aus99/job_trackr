from django.db import models
from django.forms import JSONField


class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100000)
    location = models.CharField(max_length=100, default='London')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"


class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    applied_date = models.DateField(auto_now_add=True)
    screen_date = models.DateField(null=True, blank=True)
    interview_date = models.DateField(null=True, blank=True)
    offer_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.job.title} - {self.status}"


class Report(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    logo = models.URLField()
    description = models.TextField()
    min_salary = models.DecimalField(max_digits=10, decimal_places=2)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2)
    median_salary = models.DecimalField(max_digits=10, decimal_places=2)
    salary_currency = models.CharField(max_length=10)
    sector = models.CharField(max_length=255, null=True, blank=True)
    projects = models.TextField()
    website_url = models.URLField(max_length=1024)
    total_reviews = models.IntegerField(default=0, null=True, blank=True)
    overall_rating = models.FloatField(default=0.0, null=True, blank=True)
    rating_distribution = models.JSONField(default=dict, null=True, blank=True)
    top_reviews = models.JSONField(default=list, null=True, blank=True)

    def __str__(self):
        return f"{self.company_name} - {self.job_title}"


class NewsItem(models.Model):
    report = models.ForeignKey('Report', related_name='news_items', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    snippet = models.TextField()
    url = models.URLField()

    def __str__(self):
        return f"{self.title}"
