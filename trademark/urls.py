from django.urls import path
from .views import trademark_submission_view,view_trademarks,trademark_brief,logout,view_recent,submission_list,staff_submission_view, staff_trademark, waiting_view, waiting_trademark
from django.shortcuts import render

app_name="trademark"

urlpatterns = [
    path("about-trademarks/", trademark_brief, name="trademark_brief"),
    path("trademark-submission/", trademark_submission_view, name="trademark_submission"),
    path("submission-success/", lambda request: render(request, "trademark/success.html"), name="submission_success"),
    path("approved-trademarks/", view_trademarks, name="view_trademarks"),
    path('trademark/<str:title>/view_recent/', view_recent, name='view_recent'),
    path("staff-trademark-filing/", staff_trademark, name="staff_trademark"),
    path("staff-trademark-waiting/", waiting_trademark, name="waiting_trademark"),
    path("staff/<str:title>/waiting/", waiting_view, name="staff_waiting"),
    path("staff/<str:title>/submission/", staff_submission_view, name="staff_submission"),
    path("submission-list/", submission_list, name="submission_list"),
    path('end-session/', logout, name='logout'),
]
