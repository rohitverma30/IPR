from django.db import models
from django.conf import settings
import os

class PatentSubmission(models.Model):

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
    

class Patent(models.Model):
    patentsubmission = models.ForeignKey(PatentSubmission, on_delete=models.SET_DEFAULT, default=1)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    title = models.CharField(max_length=200,unique=True)
    description = models.TextField()
    content = models.TextField()
    email = models.EmailField()
    verified_by = models.CharField(max_length=100)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} {self.content} {self.verified_by}"
    
    def save(self, *args, **kwargs):
        if self.patentsubmission:
            self.name = self.patentsubmission.name  # Auto-fill name from PatentSubmission
        super().save(*args, **kwargs)