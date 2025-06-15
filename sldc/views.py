from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import sldcSubmissionForm, StaffsldcForm, StatusForm
from .models import sldcSubmission
from .models import sldc as sldc_file
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
def sldc_submission_view(request):
    if request.method == "POST":
        form = sldcSubmissionForm(request.POST)
        if form.is_valid():
            sldcSubmission.objects.create(**form.cleaned_data)
            return redirect("sldc:submission_success")  
    else:
        form = sldcSubmissionForm()
    
    return render(request, "sldc/sldc_form.html", {"form": form})

def sldc_brief(request):
    images = banner_img.objects.all()
    random_image = random.choice(images) if images else None
    return render(request,"sldc/sldc_brief.html", {'random_image': random_image})

@login_required
def view_sldcs(request):
    query = request.GET.get('q', '')
    sldcs = sldc_file.objects.all()
    return render(request, "sldc/sldc.html", {"sldcs": sldcs,'query':query})

@login_required
def submission_list(request):
    sldcs = sldcSubmission.objects.filter(email=request.user.email)
    return render(request, "sldc/submission_list.html", {"sldcs": sldcs})

def view_recent(request, title):
    sldc = get_object_or_404(sldc_file,title=title)
    images = banner_img.objects.all()
    random_image = random.choice(images) if images else None
    return render(request, 'sldc/view_sldc.html',{'sldcs':sldc,'random_image': random_image})

#for easier handling of requests
@login_required
def staff_sldc(request):
    if request.user.role=="staff" or request.user.role=="Staff" and sldcSubmission.objects.filter(email=request.user.email,role='sldc'):
        sldcs = sldcSubmission.objects.filter(status='waiting')|sldcSubmission.objects.filter(status='unavailable')|sldcSubmission.objects.filter(status='under inspection')
        return render(request, "sldc/staff_sldc.html", {"sldcs": sldcs})
    else:
        return redirect('users:home')
@login_required
def staff_submission_view(request,title):
    if request.method == "POST":
        form = StaffsldcForm(request.POST)
        
        
        sldc = get_object_or_404(sldcSubmission,title=title)
        
        if form.is_valid():
            description=form.cleaned_data['description']
            content=form.cleaned_data['content']
            name=form.cleaned_data['name']
            sldc_edit=sldc_file.objects.create(name=name,surname=sldc.surname,email=sldc.email,title=title,description=description,content=content)
            sldc_edit.save()
            return redirect("sldc:submission_success")
    else:
        form = StaffsldcForm()
        sldc = get_object_or_404(sldcSubmission,title=title)
    return render(request, "sldc/staff_sldc_form.html", {"form": form})

@login_required
def waiting_sldc(request):
    if request.user.role=="staff" or request.user.role=="Staff" and sldcSubmission.objects.filter(email=request.user.email,role='sldc'):
        sldcs = sldcSubmission.objects.filter(status='waiting')|sldcSubmission.objects.filter(status='unavailable')
        return render(request, "sldc/staff_waiting_list.html", {"sldcs": sldcs})
    else:
        return redirect('users:home')

@login_required
def waiting_view(request,title):
    if request.method == "POST":
        form = StatusForm(request.POST)
        
        sldc = get_object_or_404(sldcSubmission,title=title)
        sldc_edit=sldcSubmission.objects.get(title=title)
        if form.is_valid():
            status=form.cleaned_data['status']
            sldc_edit.status=status
            sldc_edit.save()
            return redirect("sldc:submission_success")  
    else:
        form = StatusForm()
        sldc = get_object_or_404(sldcSubmission,title=title)
    return render(request, "sldc/staff_waiting.html", {"form": form,'email':sldc.email,'status':sldc.status})