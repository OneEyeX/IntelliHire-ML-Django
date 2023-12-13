from company.models import Company
from django.db import models
from users.models import User


# Create your models here.
class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Job(models.Model):
    job_type_choices = (
        ("Remote", "Remote"),
        ("Onsite", "Onsite"),
        ("Hybrid", "Hybrid"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    salary = models.PositiveIntegerField(default=1200)
    requirements = models.TextField()
    ideal_candidate = models.TextField()
    is_available = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    industry = models.ForeignKey(
        Industry, null=True, blank=True, on_delete=models.DO_NOTHING
    )
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.DO_NOTHING)
    job_type = models.CharField(
        max_length=20, null=True, blank=True, choices=job_type_choices
    )

    def __str__(self):
        return self.title


class ApplyJob(models.Model):
    status_choices = (
        ("Accepted", "Accepted"),
        ("Declined", "Declined"),
        ("Pending", "Pending"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    matching_value = models.FloatField(null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=status_choices)
