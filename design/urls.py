from django.urls import path
from .views import design_submission_view,view_designs,design_brief,view_recent,submission_list,staff_submission_view,staff_design, waiting_view, waiting_design
from django.shortcuts import render

app_name="design"

urlpatterns = [
    path("about-designs/", design_brief, name="design_brief"),
    path("design-submission/", design_submission_view, name="design_submission"),
    path("submission-success/", lambda request: render(request, "design/success.html"), name="submission_success"),
    path('design/<str:title>/view_recent/', view_recent, name='view_recent'),
    path("submission-list/", submission_list, name="submission_list"),
    path("staff-design-filing/", staff_design, name="staff_design"),
    path("staff-design-waiting/", waiting_design, name="waiting_design"),
    path("staff/<str:title>/waiting/", waiting_view, name="staff_waiting"),
    path("staff/<str:title>/submission/", staff_submission_view, name="staff_submission"),
    path("approved-designs/", view_designs, name="view_designs"),
]
