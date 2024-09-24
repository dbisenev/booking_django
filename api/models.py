from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Resource(models.Model):
    name = models.CharField(max_length=255)
    max_capacity = models.PositiveIntegerField()
    slots = models.JSONField()

class Booking(models.Model):
    status_choices = [
        ('active', 'Active'),
        ('waiting', 'Waiting'),
        ('completed', 'Completed')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=status_choices, default='active')