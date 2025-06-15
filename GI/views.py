from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import GISubmissionForm, StaffGIForm, StatusForm
from .models import GISubmission
from .models import GI as GI_file
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
def GI_submission_view(request):
    if request.method == "POST":
        form = GISubmissionForm(request.POST)
        if form.is_valid():
            GISubmission.objects.create(**form.cleaned_data)
            return redirect("GI:submission_success")  
    else:
        form = GISubmissionForm()
    
    return render(request, "GI/GI_form.html", {"form": form})

def GI_brief(request):
    images = banner_img.objects.all()
    random_image = random.choice(images) if images else None
    return render(request,"GI/GI_brief.html", {'random_image': random_image})

@login_required
def view_GIs(request):
    query = request.GET.get('q', '')
    GIs = GI_file.objects.all()
    return render(request, "GI/GI.html", {"GIs": GIs,'query':query})

@login_required
def submission_list(request):
    GIs = GISubmission.objects.filter(email=request.user.email)
    return render(request, "GI/submission_list.html", {"GIs": GIs})

def view_recent(request, title):
    GI = get_object_or_404(GI_file,title=title)
    #from django.shortcuts import get_object_or_404
    images = banner_img.objects.all()
    random_image = random.choice(images) if images else None
    return render(request, 'GI/view_GI.html',{'GIs':GI,'random_image': random_image})

#for easier handling of requests
@login_required
def staff_GI(request):
    if request.user.role=="staff" or request.user.role=="Staff" and GISubmission.objects.filter(email=request.user.email,role='GI'):
        GIs = GISubmission.objects.filter(status='waiting')|GISubmission.objects.filter(status='unavailable')|GISubmission.objects.filter(status='under inspection')
        return render(request, "GI/staff_GI.html", {"GIs": GIs})
    else:
        return redirect('users:home')
@login_required
def staff_submission_view(request,title):
    if request.method == "POST":
        form = StaffGIForm(request.POST)
        
        
        GI = get_object_or_404(GISubmission,title=title)
        
        if form.is_valid():
            description=form.cleaned_data['description']
            content=form.cleaned_data['content']
            name=form.cleaned_data['name']
            GI_edit=GI_file.objects.create(name=name,surname=GI.surname,email=GI.email,title=title,description=description,content=content)
            GI_edit.save()
            return redirect("GI:submission_success")
    else:
        form = StaffGIForm()
        GI = get_object_or_404(GISubmission,title=title)
    return render(request, "GI/staff_GI_form.html", {"form": form})

@login_required
def waiting_GI(request):
    if request.user.role=="staff" or request.user.role=="Staff" and GISubmission.objects.filter(email=request.user.email,role='GI'):
        GIs = GISubmission.objects.filter(status='waiting')|GISubmission.objects.filter(status='unavailable')
        return render(request, "GI/staff_waiting_list.html", {"GIs": GIs})
    else:
        return redirect('users:home')

@login_required
def waiting_view(request,title):
    if request.method == "POST":
        form = StatusForm(request.POST)
        
        GI = get_object_or_404(GISubmission,title=title)
        GI_edit=GISubmission.objects.get(title=title)
        if form.is_valid():
            status=form.cleaned_data['status']
            GI_edit.status=status
            GI_edit.save()
            return redirect("GI:submission_success")  
    else:
        form = StatusForm()
        GI = get_object_or_404(GISubmission,title=title)
    return render(request, "GI/staff_waiting.html", {"form": form,'email':GI.email, 'status':GI.status})