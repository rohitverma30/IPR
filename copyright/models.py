from django.db import models
from django.conf import settings
import os

class copyrightSubmission(models.Model):
    
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    title = models.CharField(max_length=200,unique=True)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status_CHOICES = [
        ('waiting', 'Waiting'),
        ('unavailable', 'Unavailable'),
        ('under inspection', 'Under inspection'),
        ('verified', 'Verified'),
    ]

    status = models.CharField(max_length=20, choices=status_CHOICES, default='waiting')

    def __str__(self):
        return f"{self.title} by {self.name} {self.surname}"


class banner_img(models.Model):
    image = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return f"Image {self.id}"
    

class copyright(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    title = models.CharField(max_length=200,unique=True)
    content = models.TextField()
    description = models.TextField()
    email = models.EmailField()
    verified_by = models.CharField(max_length=100)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} {self.content} {self.verified_by}"