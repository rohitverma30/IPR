from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import designSubmissionForm, StaffdesignForm, StatusForm
from .models import designSubmission
from .models import design as Design_file
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
def design_submission_view(request):
    if request.method == "POST":
        form = designSubmissionForm(request.POST)
        if form.is_valid():
            designSubmission.objects.create(**form.cleaned_data)
            return redirect("design:submission_success")  
    else:
        form = designSubmissionForm()
    
    return render(request, "design/design_form.html", {"form": form})

def design_brief(request):
    images = banner_img.objects.all()
    random_image = random.choice(images) if images else None
    return render(request,"design/design_brief.html", {'random_image': random_image})

@login_required
def view_designs(request):
    query = request.GET.get('q', '')
    designs = Design_file.objects.all()
    return render(request, "design/design.html", {"designs": designs,'query':query})

@login_required
def submission_list(request):
    designs = designSubmission.objects.filter(email=request.user.email)
    return render(request, "design/submission_list.html", {"designs": designs})

def view_recent(request, title):
    designs = get_object_or_404(Design_file,title=title)
    images = banner_img.objects.all()
    random_image = random.choice(images) if images else None
    return render(request, 'design/view_design.html',{'designs':designs,'random_image': random_image})

#for easier handling of requests
@login_required
def staff_design(request):
    if request.user.role=="staff" or request.user.role=="Staff" and designSubmission.objects.filter(email=request.user.email,role='design'):
        designs = designSubmission.objects.filter(status='waiting')|designSubmission.objects.filter(status='unavailable')|designSubmission.objects.filter(status='under inspection')
        return render(request, "design/staff_design.html", {"designs": designs})
    else:
        return redirect('users:home')
@login_required
def staff_submission_view(request,title):
    if request.method == "POST":
        form = StaffdesignForm(request.POST)
        
        
        design = get_object_or_404(designSubmission,title=title)
        
        if form.is_valid():
            description=form.cleaned_data['description']
            content=form.cleaned_data['content']
            name=form.cleaned_data['name']
            design_edit=Design_file.objects.create(name=name,surname=design.surname,email=design.email,title=title,description=description,content=content)
            design_edit.save()
            return redirect("design:submission_success")
    else:
        form = StaffdesignForm()
        design = get_object_or_404(designSubmission,title=title)
    return render(request, "design/staff_design_form.html", {"form": form})

@login_required
def waiting_design(request):
    if request.user.role=="staff" or request.user.role=="Staff" and designSubmission.objects.filter(email=request.user.email,role='design'):
        designs = designSubmission.objects.filter(status='waiting')|designSubmission.objects.filter(status='unavailable')
        return render(request, "design/staff_waiting_list.html", {"designs": designs})
    else:
        return redirect('users:home')

@login_required
def waiting_view(request,title):
    if request.method == "POST":
        form = StatusForm(request.POST)
        
        design = get_object_or_404(designSubmission,title=title)
        design_edit=designSubmission.objects.get(title=title)
        if form.is_valid():
            status=form.cleaned_data['status']
            design_edit.status=status
            design_edit.save()
            return redirect("design:submission_success")  
    else:
        form = StatusForm()
        design = get_object_or_404(designSubmission,title=title)
    return render(request, "design/staff_waiting.html", {"form": form,'email':design.email,'status':design.status})