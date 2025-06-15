from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PatentSubmissionForm, StaffPatentForm, StatusForm
from .models import PatentSubmission
from .models import Patent as Patent_file
from .models import banner_img
import random
from django.shortcuts import get_object_or_404
from users.forms import LoginForm
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:write_blog')  
            else:
                return render(request, 'users/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def patent_submission_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email != request.user.email:
            return redirect("patent:error_page")
            #return redirect('patent:error-message')

        form = PatentSubmissionForm(request.POST)
        if form.is_valid():
            PatentSubmission.objects.create(**form.cleaned_data)
            return redirect("patent:submission_success")  
    else:
        form = PatentSubmissionForm()
    
    return render(request, "patent/patent_form.html", {"form": form})

def patent_brief(request):
    images = banner_img.objects.all()
    random_image = random.choice(images) if images else None
    return render(request,"patent/patent_brief.html", {'random_image': random_image})

@login_required
def view_patents(request):
    query = request.GET.get('q', '')
    patents = Patent_file.objects.all()
    return render(request, "patent/patent.html", {"patents": patents,'query':query})

@login_required
def submission_list(request):
    patents = PatentSubmission.objects.filter(email=request.user.email)
    return render(request, "patent/submission_list.html", {"patents": patents})
#for easier handling of requests
@login_required
def staff_patent(request):
    if request.user.role=="staff" or request.user.role=="Staff" and PatentSubmission.objects.filter(email=request.user.email,role='patent'):
        patents = PatentSubmission.objects.filter(status='waiting')|PatentSubmission.objects.filter(status='unavailable')|PatentSubmission.objects.filter(status='under inspection')
        return render(request, "patent/staff_patent.html", {"patents": patents})
    else:
        return redirect('users:home')
@login_required
def staff_submission_view(request,title):
    if request.method == "POST":
        form = StaffPatentForm(request.POST)
        
        
        patent = get_object_or_404(PatentSubmission,title=title)
        
        if form.is_valid():
            description=form.cleaned_data['description']
            content=form.cleaned_data['content']
            name=form.cleaned_data['name']
            patent_edit=Patent_file.objects.create(name=name,surname=patent.surname,email=patent.email,title=title,description=description,content=content)
            patent_edit.save()
            return redirect("patent:submission_success")
    else:
        form = StaffPatentForm()
        patent = get_object_or_404(PatentSubmission,title=title)
    return render(request, "patent/staff_patent_form.html", {"form": form})

@login_required
def waiting_patent(request):
    if request.user.role=="staff" or request.user.role=="Staff" and PatentSubmission.objects.filter(email=request.user.email,role='patent'):
        patents = PatentSubmission.objects.filter(status='waiting')|PatentSubmission.objects.filter(status='unavailable')
        return render(request, "patent/staff_waiting_list.html", {"patents": patents})
    else:
        return redirect('users:home')

@login_required
def waiting_view(request,title):
    if request.method == "POST":
        form = StatusForm(request.POST)
        
        patent = get_object_or_404(PatentSubmission,title=title)
        patent_edit=PatentSubmission.objects.get(title=title)
        if form.is_valid():
            status=form.cleaned_data['status']
            patent_edit.status=status
            patent_edit.save()
            return redirect("patent:submission_success")  
    else:
        form = StatusForm()
        patent = get_object_or_404(PatentSubmission,title=title)
    return render(request, "patent/staff_waiting.html", {"form": form,'email':patent.email, 'status':patent.status})

def view_recent(request, title):
    patent = get_object_or_404(Patent_file,title=title)
    #from django.shortcuts import get_object_or_404
    images = banner_img.objects.all()
    random_image = random.choice(images) if images else None
    return render(request, 'patent/view_patent.html',{'patents':patent,'random_image': random_image})
