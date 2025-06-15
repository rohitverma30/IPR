from django.urls import path
from .views import copyright_submission_view,view_copyrights,copyright_brief,view_recent,submission_list,staff_submission_view,staff_copyright,waiting_copyright,waiting_view
from django.shortcuts import render

app_name="copyright"

urlpatterns = [
    path("about-copyrights/", copyright_brief, name="copyright_brief"),
    path("copyright-submission/", copyright_submission_view, name="copyright_submission"),
    path("submission-success/", lambda request: render(request, "copyright/success.html"), name="submission_success"),
    path('copyright/<str:title>/view_recent/', view_recent, name='view_recent'),
    path("submission-list/", submission_list, name="submission_list"),
    path("staff-copyright-filing/", staff_copyright, name="staff_copyright"),
    path("staff-copyright-waiting/", waiting_copyright, name="waiting_copyright"),
    path("staff/<str:title>/waiting/", waiting_view, name="staff_waiting"),
    path("staff/<str:title>/submission/", staff_submission_view, name="staff_submission"),
    path("approved-copyrights/", view_copyrights, name="view_copyrights"),
]
