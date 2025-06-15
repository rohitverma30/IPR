from django.urls import path
from .views import register_view, login_view, home_view, write_blog, about_us, logout, view_blog, view_all, edit_blog,all_blogs, view_selected, view_recent, manage_blog,contact_us_submission_view
from django.shortcuts import render
app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('',home_view,name='home'),
    path('write_blog/', write_blog, name='write_blog'),
    path('view_blog/', view_blog, name='view_blog'),
    path('all_blogs/', all_blogs, name='all_blogs'),
    path('about_us/', about_us, name='about_us'),
    path('contact_us/', contact_us_submission_view, name='contact_us'),
    path("submission-success/", lambda request: render(request, "users/success.html"), name="submission_success"),
    path("terms-and-conditions/", lambda request: render(request, "users/termsconditions.html"), name="termsconditions"),
    path('end-session/', logout, name='logout'),
    path('blog/<int:blog_id>/edit/', edit_blog, name='edit_blog'),
    path('blog/<int:blog_id>/view_selected', view_selected, name='view_selected'),
    path('blog/<int:blog_id>/view_all', view_all, name='view_all'),
    path('blog/<int:user_id>/<str:title>/view_recent/', view_recent, name='view_recent'),
    path('manage_blog/', manage_blog, name='manage_blog'),
    #path("error-page/", error_page, name="error_page"),
]
