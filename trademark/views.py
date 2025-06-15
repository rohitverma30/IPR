from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import trademarkSubmissionForm, StafftrademarkForm, StatusForm
from .models import trademarkSubmission
from .models import trademark as Trademark_file
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
def trademark_submission_view(request):
    if request.method == "POST":
        form = trademarkSubmissionForm(request.POST)
        if form.is_valid():
            trademarkSubmission.objects.create(**form.cleaned_data)
            return redirect("trademark:submission_success")  
    else:
        form = trademarkSubmissionForm()
    
    return render(request, "trademark/trademark_form.html", {"form": form})

def trademark_brief(request):
    images = banner_img.objects.all()
    random_image = random.choice(images) if images else None
    return render(request,"trademark/trademark_brief.html", {'random_image': random_image})

@login_required
def view_trademarks(request):
    query = request.GET.get('q', '')
    trademarks = Trademark_file.objects.all()
    return render(request, "trademark/trademark.html", {"trademarks": trademarks,'query':query})


@login_required
def logout(request):
    request.session.flush()  
    return redirect('users:login') 

@login_required
def submission_list(request):
    trademarks = trademarkSubmission.objects.filter(email=request.user.email)
    return render(request, "trademark/submission_list.html", {"trademarks": trademarks})

def view_recent(request, title):
    trademark = get_object_or_404(Trademark_file,title=title)
    images = banner_img.objects.all()
    random_image = random.choice(images) if images else None
    return render(request, 'trademark/view_trademark.html',{'trademarks':trademark,'random_image': random_image})

#for easier handling of requests
@login_required
def staff_trademark(request):
    if request.user.role=="staff" or request.user.role=="Staff" and trademarkSubmission.objects.filter(email=request.user.email,role='trademark'):
        trademarks = trademarkSubmission.objects.filter(status='waiting')|trademarkSubmission.objects.filter(status='unavailable')|trademarkSubmission.objects.filter(status='under inspection')
        return render(request, "trademark/staff_trademark.html", {"trademarks": trademarks})
    else:
        return redirect('users:home')
@login_required
def staff_submission_view(request,title):
    if request.method == "POST":
        form = StafftrademarkForm(request.POST)
        
        
        trademark = get_object_or_404(trademarkSubmission,title=title)
        
        if form.is_valid():
            description=form.cleaned_data['description']
            content=form.cleaned_data['content']
            name=form.cleaned_data['name']
            trademark_edit=Trademark_file.objects.create(name=name,surname=trademark.surname,email=trademark.email,title=title,description=description,content=content)
            trademark_edit.save()
            return redirect("trademark:submission_success")
    else:
        form = StafftrademarkForm()
        trademark = get_object_or_404(trademarkSubmission,title=title)
    return render(request, "trademark/staff_trademark_form.html", {"form": form})

@login_required
def waiting_trademark(request):
    if request.user.role=="staff" or request.user.role=="Staff" and trademarkSubmission.objects.filter(email=request.user.email,role='trademark'):
        trademarks = trademarkSubmission.objects.filter(status='waiting')|trademarkSubmission.objects.filter(status='unavailable')
        return render(request, "trademark/staff_waiting_list.html", {"trademarks": trademarks})
    else:
        return redirect('users:home')

@login_required
def waiting_view(request,title):
    if request.method == "POST":
        form = StatusForm(request.POST)
        
        trademark = get_object_or_404(trademarkSubmission,title=title)
        
        trademark_edit=trademarkSubmission.objects.get(title=title)
        if form.is_valid():
            status=form.cleaned_data['status']
            trademark_edit.status=status
            trademark_edit.save()
            return redirect("trademark:submission_success")  
    else:
        form = StatusForm()
        trademark = get_object_or_404(trademarkSubmission,title=title)
    return render(request, "trademark/staff_waiting.html", {"form": form,'email':trademark.email,'status':trademark.status})