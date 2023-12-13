from django.shortcuts import redirect, render
from job.models import ApplyJob, Job

# Create your views here.
# def proxy(request):
#     if request.user.is_applicant:
#         return redirect("applicant-dashboard")
#     elif request.user.is_recruiter:
#         return redirect("recruiter-dashboard")
#     else:
#         return redirect("login")


# def applicant_dashboard(request):
#     return render("dashboard/applicant_dashboard.html")


# def recruiter_dashboard(request):
#     return render("dashboard/recruiter_dashboard.html")


def dashboard(request):
    context = {}
    if request.user.is_applicant:
        jobs = ApplyJob.objects.filter(user=request.user)
        context = {
            "jobs": jobs,
        }
    if request.user.is_recruiter:
        jobs = Job.objects.filter(user=request.user, company=request.user.company)
        context = {"jobs": jobs}

    return render(request, "dashboard/dashboard.html", context)
