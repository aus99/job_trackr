from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    location = models.CharField(max_length=100, default='London')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

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
