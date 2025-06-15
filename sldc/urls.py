from django.urls import path
from .views import sldc_submission_view,view_sldcs,sldc_brief,view_recent,submission_list,staff_sldc, staff_submission_view, waiting_sldc, waiting_view
from django.shortcuts import render

app_name="sldc"

urlpatterns = [
    path("about-sldcs/", sldc_brief, name="sldc_brief"),
    path("sldc-submission/", sldc_submission_view, name="sldc_submission"),
    path("submission-success/", lambda request: render(request, "sldc/success.html"), name="submission_success"),
    path('sldc/<str:title>/view_recent/', view_recent, name='view_recent'),
    path("submission-list/", submission_list, name="submission_list"),
    path("staff-sldc-filing/", staff_sldc, name="staff_sldc"),
    path("staff-sldc-waiting/", waiting_sldc, name="waiting_sldc"),
    path("staff/<str:title>/waiting/", waiting_view, name="staff_waiting"),
    path("staff/<str:title>/submission/", staff_submission_view, name="staff_submission"),
    path("approved-sldcs/", view_sldcs, name="view_sldcs"),
]
