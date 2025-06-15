from django import forms
from .models import Blog
from django import forms
from django import forms
from .models import CustomUser
from .models import InternEmail, StaffEmail
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,  # Ensure choices are loaded correctly
        widget=forms.RadioSelect,
        required=True
    )
   
    staff_role = forms.ChoiceField(
        choices=StaffEmail.STAFF_ROLE,  # Ensure choices are loaded correctly
        widget=forms.RadioSelect(attrs={'class': 'blog-titlearea'}),
        
        required=False,
        label="If you are staff make sure you select the one of the choices if not please leave it blank"
    )
   

    key=forms.IntegerField(required=False,label="passkey")
    consent_given = forms.BooleanField(required=True, label="I agree to the terms and conditions")
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role', 'staff_role' ,'key', 'consent_given']


            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        role = self.cleaned_data.get('role')
        
        # Check email existence in InternEmail table only if role is 'intern'
        if role == 'intern' and not InternEmail.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is not authorized for an intern account.")
        if role == 'staff' and not StaffEmail.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is not authorized for an staff account.")
        return email

"""

if form.is_valid():
    user = form.save(commit=False)
    user.set_password(form.cleaned_data['password'])
    user.role = form.cleaned_data['role']  # Explicitly set role
    user.save()
------------------------
    if form.is_valid():
    user = form.save(commit=False)
    user.set_password(form.cleaned_data['password'])
    print(f"User role before saving: {user.role}")  # Debugging
    user.save()

"""


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        widgets = {
            'username': forms.TextInput(attrs={'class': '.Loginform_input', 'placeholder': 'Enter username'}),
            'email': forms.TextInput(attrs={'class': '.Loginform_input', 'placeholder': 'Enter your email  address here'}),
            
        }


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description','content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'blog-titlearea', 'placeholder': 'Enter blog title'}),
            'description': forms.TextInput(attrs={'class': 'blog-titlearea', 'placeholder': 'Write your description here...'}),
            'content': forms.Textarea(attrs={'class': 'blog-textarea', 'placeholder': 'Write your content here...'}),
        }


class BlogEditForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'blog-titlearea', 'placeholder': 'Enter blog title'}),
            'content': forms.Textarea(attrs={'class': 'blog-textarea', 'placeholder': 'Edit your content here...'}),
        }

class contact_usSubmissionForm(forms.Form):
    name = forms.CharField(label="First Name", max_length=100, required=True)
    surname = forms.CharField(label="Surname", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    phone = forms.CharField(label="Phone Number", max_length=10, required=True, widget=forms.TextInput(attrs={'pattern': '[0-9]{10}', 'title': 'Enter a valid 10-digit phone number'}))
    title = forms.CharField(label="Title of contact us", max_length=200, required=True)
    description = forms.CharField(label="Description of contact us", widget=forms.Textarea, required=True)
