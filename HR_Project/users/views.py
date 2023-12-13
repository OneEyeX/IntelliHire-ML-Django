from company.models import Company
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from resume.models import Resume

from .form import RegisterUserForm
from .models import User

# Create your views here.


# register applicant
def register_applicant(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_applicant = True
            var.username = var.email
            var.save()
            Resume.objects.create(user=var)
            messages.info(request, "Your account has been created. Please Login")
            return redirect("login")
        else:
            messages.warning(request, "Something went wrong")
            return redirect("register-applicant")
    else:
        form = RegisterUserForm()
        context = {"form": form}
        return render(request, "users/register_applicant.html", context)


# register recruiter only
def register_recruiter(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_recruiter = True
            var.username = var.email
            var.save()
            Company.objects.create(user=var)
            messages.info(request, "Your account has been created. Please Login")
            return redirect("login")
        else:
            messages.warning(request, "Something went wrong")
            return redirect("register-recruiter")
    else:
        form = RegisterUserForm()
        context = {"form": form}
        return render(request, "users/register_recruiter.html", context)


# login a user
def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(
            request,
            username=email,
            password=password,
        )
        if user is not None and user.is_active:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.warning(request, "something went wrong")
            return redirect("login")
    else:
        return render(
            request,
            "users/login.html",
        )


# logout user
def logout_user(request):
    logout(request)
    messages.info(request, "your session has been ended")
    return redirect("login")
