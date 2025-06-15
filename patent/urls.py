from django.urls import path
from .views import patent_submission_view,view_patents,patent_brief, view_recent, submission_list, staff_patent,staff_submission_view,waiting_view, waiting_patent
from django.shortcuts import render

app_name="patent"

urlpatterns = [
    path("about-patents/", patent_brief, name="patent_brief"),
    path("patent-submission/", patent_submission_view, name="patent_submission"),
    path("submission-success/", lambda request: render(request, "patent/success.html"), name="submission_success"),
    path('patent/<str:title>/view_recent/', view_recent, name='view_recent'),
    path("approved-patents/", view_patents, name="view_patents"),
    path("submission-list/", submission_list, name="submission_list"),
    path("staff-patent-filing/", staff_patent, name="staff_patent"),
    path("staff-patent-waiting/", waiting_patent, name="waiting_patent"),
    path("staff/<str:title>/waiting/", waiting_view, name="staff_waiting"),
    path("staff/<str:title>/submission/", staff_submission_view, name="staff_submission"),
    path("error-page/", lambda request: render(request, "patent/error-page.html"), name="error_page"),
]
