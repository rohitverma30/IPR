from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.db.models import UniqueConstraint
import random
User = settings.AUTH_USER_MODEL

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('intern', 'Intern'),
        ('staff', 'Staff'),
    ]
    

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    
    
    
    # Fix clashes by adding related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Change related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Change related name
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
    class Meta:
        constraints = [
            UniqueConstraint(fields=['email'], name='unique_email_constraint')
        ]


class PageView(models.Model):
    url = models.CharField(max_length=255)  # Track views per page
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.url}: {self.count} views"


class Blog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blogs'
    )
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)
    visibility=models.BooleanField(default=True)
    class Meta:
        ordering = ['-created_at']
class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='team_photos/')

    def __str__(self):
        return self.name

class SlideshowImage(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True) 
    image = models.ImageField(upload_to='slideshow_images/')  
    order = models.PositiveIntegerField(default=0)  
    uploaded_at = models.DateTimeField(auto_now_add=True)  

    class Meta:
        ordering = ['order']  

    def __str__(self):
        return self.title or f"Image {self.id}"

class Pass_key(models.Model):
    email = models.EmailField(unique=True)
    pass_code=models.IntegerField(unique=True, default=8790)

    def __str__(self):
        return self.email
    
class InternEmail(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class StaffEmail(models.Model):
    #for easier handling of requests
    
    STAFF_ROLE=[
        ('patent','Patent'),
        ('trademark','Trademark'),
        ('copyright','Copyright'),
        ('gi','GI'),
        ('sicld','SICLD'),
        ('design','Design'),
        ('blogging','Blogging'),  
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=12, choices=STAFF_ROLE, default='blogging')
    def __str__(self):
        return self.email

class News(models.Model):
    news=models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at'] 
    
    def __str__(self):
        return self.news
    
class contact_usSubmission(models.Model):
    
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
