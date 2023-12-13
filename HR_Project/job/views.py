import pandas as pd
from django.contrib import messages
from django.shortcuts import redirect, render
from resume.models import Resume

from .form import CreateJobForm, UpdateJobForm
from .models import ApplyJob, Job
from .recommend_job import get_jobs_recommendations


# Create your views here.
# create a job
def create_job(request):
    if request.user.is_recruiter and request.user.has_company:
        if request.method == "POST":
            form = CreateJobForm(request.POST)
            if form.is_valid():
                var = form.save(commit=False)
                var.user = request.user
                var.company = request.user.company
                var.save()
                messages.info(request, "New Job has been created successfully")
                return redirect("dashboard")
            else:
                messages.warning(request, "something went wrong")
        else:
            form = CreateJobForm()
            context = {"form": form}
            return render(
                request,
                "job/create_job.html",
                context,
            )
    else:
        messages.warning(request, "Permission denied")
        return redirect("dashboard")


# update a job
def update_job(request, pk):
    job = Job.objects.get(pk=pk)
    if request.method == "POST":
        form = UpdateJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.info(request, "Job has been updated successfully")
            return redirect("dashboard")
        else:
            messages.warning(request, "something went wrong")
    else:
        form = UpdateJobForm(instance=job)
        context = {"form": form}
        return render(
            request,
            "job/update_job.html",
            context,
        )


#
def manage_jobs(request):
    jobs = Job.objects.filter(user=request.user, company=request.user.company)
    context = {"jobs": jobs}
    return render(
        request,
        "job/manage_jobs.html",
        context,
    )


def apply_to_job(request, pk):
    if request.user.is_authenticated and request.user.is_applicant:
        job = Job.objects.get(pk=pk)
        if ApplyJob.objects.filter(user=request.user, job=pk).exists():
            messages.warning(request, "Permission denied")
            return redirect("dashboard")
        else:
            d = {
                "id": job.pk,
                "title": job.title,
                "salary": job.salary,
                "job_type": job.job_type,
                "job_requirements": job.requirements,
                "requirements": job.requirements,
            }
            # transform the dict to a pandas dataframe
            df = pd.DataFrame([d])
            # print(df)

            # retrieve the skills for the current user from the database
            s = {"skills": request.user.resume.skills}
            # print("tttt")
            print(get_jobs_recommendations(df, s, nb=1)[1])

            #
            ApplyJob.objects.create(
                job=job,
                user=request.user,
                status="Pending",
                matching_value=round(get_jobs_recommendations(df, s, nb=1)[1], 2),
            )
            messages.info(request, "You have successfully applied to this job")
            return redirect("dashboard")
    else:
        messages.info(request, "Please login to continue")
        return redirect("login")


# all applicants view
def all_applicants(request, pk):
    job = Job.objects.get(pk=pk)
    applicants = job.applyjob_set.all().order_by("-matching_value")
    context = {
        "job": job,
        "applicants": applicants,
    }
    return render(
        request,
        "job/all_applicants.html",
        context,
    )


# Job recommendation view
def recommend_jobs(request, pk):
    jobs = Job.objects.all()
    # if jobs:
    df = pd.DataFrame(list(jobs.values()))
    skills = Resume.objects.filter(user=pk).values("skills").first()
    # resume = Resume.objects.filter(user=pk).values("upload_resume").first()
    # resume = resume["upload_resume"]
    # print(resume)
    df2, val = get_jobs_recommendations(df, skills, nb=5)
    # print(val[0][0])
    context = {
        "tables": df2.to_html(
            classes="table table-bordered table-hover table-sm table-responsive"
        )
    }
    return render(
        request,
        "job/recommended_job.html",
        context,
    )


def applied_jobs(request):
    jobs = ApplyJob.objects.filter(user=request.user)
    context = {"jobs": jobs}
    return render(
        request,
        "job/applied_jobs.html",
        context,
    )
