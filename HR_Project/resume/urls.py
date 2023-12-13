from django.urls import path

from . import views

urlpatterns = [
    path("update-resume/", views.update_resume, name="update-resume"),
    # path("delete-resume/", views.delete_resume, name="delete-resume"),
    path("resume-details/<int:pk>/", views.resume_details, name="resume-details"),
]
