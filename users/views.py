from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import TeamMember, Blog
from .forms import SignupForm
from .forms import LoginForm
from .forms import BlogForm
from .forms import BlogEditForm, contact_usSubmissionForm
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.urls import reverse
from .models import SlideshowImage, contact_usSubmission
from django.contrib.auth import get_user_model
from .models import InternEmail, StaffEmail, Pass_key, PageView
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import InternEmail, StaffEmail
from .forms import SignupForm
from django.contrib.auth.models import User
from .models import News
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignupForm
import logging


CustomUser=get_user_model()





def register_view(request):
    
    alert=""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.key = form.cleaned_data['key']
            user.staff_role = form.cleaned_data['staff_role']
            if user.role == 'intern' and not InternEmail.objects.filter(email=user.email).exists():
                
                alert="Your email is not authorized for an intern account."
                
                messages.error(request, alert)
                print("yes")
                return render(request, 'users/register.html', {'form': form,'error':alert})
            else:
                if InternEmail.objects.filter(email=user.email).exists() and not get_object_or_404(Pass_key, email=user.email,pass_code=user.key ) :
                    alert="Your passkey is not authorize"
                    messages.error(request, "Your passkey is not authorize")
                    return render(request, 'users/register.html', {'form': form,'error':alert})
            
            if user.role == 'staff' and not StaffEmail.objects.filter(email=user.email).exists():
                alert="Your email is not authorized for a staff account."
                messages.error(request, alert)
                return render(request, 'users/register.html', {'form': form,'error':alert})
            else:
                if StaffEmail.objects.filter(email=user.email).exists() and not get_object_or_404(Pass_key, email=user.email,pass_code=user.key ):
                    alert= "Your passkey is not authorize"
                    messages.error(request,alert)
                    return render(request, 'users/register.html', {'form': form,'error':alert})

                #for easier handling of requests
                if StaffEmail.objects.filter(email=user.email).exists() and not get_object_or_404(StaffEmail, email=user.email,role=user.staff_role ):
                    alert="You are not authorized for this role"
                    messages.error(request, alert)
                    return render(request, 'users/register.html', {'form': form,'error':alert})
            user.save()
            
            user.consent_given = form.cleaned_data["consent_given"]
            if not user.consent_given:
                return render(request, 'users/register.html', {'form': form})
            
            # Explicit authentication
            authenticated_user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            if authenticated_user:
                login(request, authenticated_user)  # Ensure login session is established
                messages.success(request, "Registration successful!")
                request.session['notification'] = "Registration successful! welcome to our site"
                

            redirect_urls = {
                'guest': 'users:home',
                'intern': 'users:write_blog',
                'staff': 'users:manage_blog'
            }

            return redirect(redirect_urls.get(user.role, 'users:view_blog'))

    else:
        form = SignupForm()
    
    return render(request, 'users/register.html', {'form': form,'error':alert})


def login_view(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Authenticate using CustomUser explicitly
            user = CustomUser.objects.filter(username=username).first()
                
            if user and user.check_password(password) :  # Use check_password for hashed passwords
                
                login(request, user)
                redirect_urls = {
                            'guest': 'users:home',
                            'intern': 'users:write_blog',
                            'staff': 'users:manage_blog'
                }
                request.session['notification'] ="logged in"
                return redirect(redirect_urls.get(user.role, 'users:all_blogs'))
                

            else:
                form.add_error(None, "Invalid username or password.")
        
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def home_view(request):
    blog=Blog.objects.filter(visibility=True)
    news=News.objects.first()
    images = SlideshowImage.objects.all()
    msg = request.session.pop('notification', None)
    
    return render(request, 'users/main.html',{'Blogs': blog,'slideshow_images': images, 'news':news,'msg': msg})


ogger = logging.getLogger(__name__)

@login_required
def write_blog(request):
    """Handles blog submission, ensuring authentication & role validation."""
    
    logger.info(f"User Debug: ID={request.user.id}, Authenticated={request.user.is_authenticated}, Role={getattr(request.user, 'role', None)}")

    # Validate user authentication
    if not request.user.is_authenticated:
        messages.error(request, "Please log in first.")
        return redirect('users:login')

    # Check if the user has permission (interns & staff only)
    user_role = getattr(request.user, "role", None)
    if user_role not in ['intern', 'staff']:
        messages.error(request, "You do not have permission to write blogs.")
        request.session['notification'] ="You do not have permission to write blogs."
        return redirect('users:home')

    # Handle blog submission
    if request.method == 'POST':
        form = BlogForm(request.POST)
        logger.error(f"Form validation errors: {form.errors.as_json()}")

        if form.is_valid():
            blog = form.save(commit=False)
            user = CustomUser.objects.get(username=request.user.username) 

            blog = Blog(
                user=user,  
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content']
            )

            
            
            if CustomUser.objects.filter(id=request.user.id).exists():
                
                blog.user = request.user
                blog.user.user_id=request.user.id
                
                
                blog.save()
                messages.success(request, "Blog posted successfully!")
                request.session['notification'] ="Blog posted successfully!"
                return redirect('users:home')
            else:
                messages.error(request, "User session error. Please log in again.")
                return redirect('users:login')
        else:
            logger.error(f"Form errors: {form.errors}")
            messages.error(request, "Blog submission failed due to invalid data.")
    else:
        form = BlogForm()

    return render(request, 'users/write_blog.html', {'form': form})

@login_required
def about_us(request):
    team_members = TeamMember.objects.all()
    
    return render(request, 'users/aboutus.html',{'TeamMember': team_members})


@login_required
def logout(request):
    request.session.flush()  
    return redirect('users:login') 

@login_required
def view_blog(request):
    if request.user.role =='guest':
        return redirect('users:all_blogs')
    blogs = Blog.objects.filter(user=request.user)
    images = SlideshowImage.objects.all()
    return render(request, 'users/view_blog.html', {'Blogs': blogs,'slideshow_images':images})
  
@login_required
def all_blogs(request):
    
    query = request.GET.get('q', '') 
    results = Blog.objects.filter(title=query, visibility=True)
    blogs=Blog.objects.all()
    return render(request, 'users/all_blog.html', {'Blogs': results, 'query': query,'all':blogs})


@login_required
def edit_blog(request, blog_id):
    
    if request.user.role in ['staff']:
        blog = get_object_or_404(Blog, id=blog_id, user=request.user)  
        if request.method == 'POST':
            form = BlogEditForm(request.POST, instance=blog)
            if form.is_valid():
                blog = form.save(commit=False)
                blog.last_edited_at = now()  
                blog.is_edited = True  
                blog.save()
                return redirect('users:view_blog')  
        else:
            form = BlogEditForm(instance=blog)  
        return render(request, 'users/edit_blog.html', {'form': form, 'blog': blog})
    else:
        request.session['notification'] ="You do not have permission to edit blog"
        return redirect('users:home')

def not_logged_in(request):
    return render(request, 'users/not_logged_in.html', {'message': 'You need to log in to access this page.'})

@login_required
def view_selected(request, blog_id):
    images = SlideshowImage.objects.all()
    random_image = random.choice(images) if images else None
    if not request.user.is_authenticated: 
        return redirect('not_logged_in')  
    blogs = get_object_or_404(Blog, id=blog_id, user=request.user)   
    return render(request, 'users/view_selected.html', {'blogs': blogs,'image':random_image})

@login_required
def view_all(request, blog_id):
    images = SlideshowImage.objects.all()
    random_image = random.choice(images) if images else None
    if not request.user.is_authenticated: 
        return redirect('not_logged_in')  
    blogs = get_object_or_404(Blog, id=blog_id)   
    return render(request, 'users/view_all.html', {'blogs': blogs,'image':random_image})


logger = logging.getLogger(__name__)

@login_required
def manage_blog(request):
    
    logger.info(f"Current User: {request.user}, Authenticated: {request.user.is_authenticated}")

    if not request.user.is_authenticated:
        messages.error(request, "Please log in first.")
        return redirect('users:login')  # Redirect to login page

    user_blogs = Blog.objects.filter(user=request.user)

    if request.user.role == 'staff':
        return render(request, 'users/render_blog.html', {'Blogs': user_blogs})
    request.session['notification'] ="You are not permitted for this page"
    return redirect('users:home')

@login_required
def view_recent(request, user_id, title):
    blog = get_object_or_404(Blog, title=title)
    images = SlideshowImage.objects.all()
    random_image = random.choice(images) if images else None
    return render(request, 'users/view_recent.html',{'blogs':blog,'image':random_image})

@login_required
def contact_us_submission_view(request):
    if request.method == "POST":
        form = contact_usSubmissionForm(request.POST)
        if form.is_valid():
            contact_usSubmission.objects.create(**form.cleaned_data)
            return redirect("users:submission_success")  
    else:
        form = contact_usSubmissionForm()
    
    return render(request, "users/contactus_form.html", {"form": form})