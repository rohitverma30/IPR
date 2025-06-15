from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import copyrightSubmissionForm, StaffcopyrightForm, StatusForm
from .models import copyrightSubmission
from .models import copyright as Copyright_file
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
def copyright_submission_view(request):
    if request.method == "POST":
        form = copyrightSubmissionForm(request.POST)
        if form.is_valid():
            copyrightSubmission.objects.create(**form.cleaned_data)
            return redirect("copyright:submission_success")  
    else:
        form = copyrightSubmissionForm()
    
    return render(request, "copyright/copyright_form.html", {"form": form})

def copyright_brief(request):
    images = banner_img.objects.all()
    random_image = random.choice(images) if images else None
    return render(request,"copyright/copyright_brief.html", {'random_image': random_image})

@login_required
def view_copyrights(request):
    query = request.GET.get('q', '')
    copyrights = Copyright_file.objects.all()
    return render(request, "copyright/copyright.html", {"copyrights": copyrights,'query':query})

@login_required
def submission_list(request):
    copyrights = copyrightSubmission.objects.filter(email=request.user.email)
    return render(request, "copyright/submission_list.html", {"copyrights": copyrights})

def view_recent(request, title):
    copyrights = get_object_or_404(Copyright_file,title=title)
    images = banner_img.objects.all()
    random_image = random.choice(images) if images else None
    return render(request, 'copyright/view_copyright.html',{'copyrights':copyrights,'random_image': random_image})

#for easier handling of requests
@login_required
def staff_copyright(request):
    if request.user.role=="staff" or request.user.role=="Staff" and copyrightSubmission.objects.filter(email=request.user.email,role='copyright'):
        copyrights = copyrightSubmission.objects.filter(status='waiting')|copyrightSubmission.objects.filter(status='unavailable')|copyrightSubmission.objects.filter(status='under inspection')
        return render(request, "copyright/staff_copyright.html", {"copyrights": copyrights})
    else:
        return redirect('users:home')
@login_required
def staff_submission_view(request,title):
    if request.method == "POST":
        form = StaffcopyrightForm(request.POST)
        
        
        copyright = get_object_or_404(copyrightSubmission,title=title)
        
        if form.is_valid():
            description=form.cleaned_data['description']
            content=form.cleaned_data['content']
            name=form.cleaned_data['name']
            copyright_edit=Copyright_file.objects.create(name=name,surname=copyright.surname,email=copyright.email,title=title,description=description,content=content)
            copyright_edit.save()
            return redirect("copyright:submission_success")
    else:
        form = StaffcopyrightForm()
        copyright = get_object_or_404(copyrightSubmission,title=title)
    return render(request, "copyright/staff_copyright_form.html", {"form": form})

@login_required
def waiting_copyright(request):
    if request.user.role=="staff" or request.user.role=="Staff" and copyrightSubmission.objects.filter(email=request.user.email,role='copyright'):
        copyrights = copyrightSubmission.objects.filter(status='waiting')|copyrightSubmission.objects.filter(status='unavailable')
        return render(request, "copyright/staff_waiting_list.html", {"copyrights": copyrights})
    else:
        return redirect('users:home')

@login_required
def waiting_view(request,title):
    if request.method == "POST":
        form = StatusForm(request.POST)
        
        copyright = get_object_or_404(copyrightSubmission,title=title)
        copyright_edit=copyrightSubmission.objects.get(title=title)
        if form.is_valid():
            status=form.cleaned_data['status']
            copyright_edit.status=status
            copyright_edit.save()
            return redirect("copyright:submission_success")  
    else:
        form = StatusForm()
        copyright = get_object_or_404(copyrightSubmission,title=title)
    return render(request, "copyright/staff_waiting.html", {"form": form,'email':copyright.email,'status':copyright.status})