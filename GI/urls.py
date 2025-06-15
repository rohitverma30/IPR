from django.urls import path
from .views import GI_submission_view,view_GIs,GI_brief,view_recent,submission_list,staff_GI,staff_submission_view, waiting_GI, waiting_view
from django.shortcuts import render

app_name="GI"

urlpatterns = [
    path("about-GIs/", GI_brief, name="GI_brief"),
    path("GI-submission/", GI_submission_view, name="GI_submission"),
    path("submission-success/", lambda request: render(request, "GI/success.html"), name="submission_success"),
    path("approved-GIs/", view_GIs, name="view_GIs"),
    path("submission-list/", submission_list, name="submission_list"),
    path("staff-GI-filing/", staff_GI, name="staff_GI"),
    path("staff-GI-waiting/", waiting_GI, name="waiting_GI"),
    path("staff/<str:title>/waiting/", waiting_view, name="staff_waiting"),
    path("staff/<str:title>/submission/", staff_submission_view, name="staff_submission"),
    path('GI/<str:title>/view_recent/', view_recent, name='view_recent'),
]
