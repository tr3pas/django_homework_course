from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import CourseFormSet, LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import StudentCourses

# Create your views here.

def index(request: HttpRequest):
    return render(request, "course/index.html")


def register_view(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        formset = CourseFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            user = form.save()
            login(request, user)
            for f in formset:
                if f.cleaned_data.get("course") or f.cleaned_data.get("priority"):
                    StudentCourses.objects.create(
                        student=user,
                        course=f.cleaned_data.get("course"),
                        priority=f.cleaned_data.get("priority")
                    )
            
            
            messages.success(request, "Реєстрація пройшла успішно!")

            return redirect("course:index")
        else:
            
            messages.error(request, "Помилка реєстрації. Будь ласка, виправте помилки у формі.")
    
    else:
        form = RegisterForm()
        formset = CourseFormSet(queryset=StudentCourses.objects.none())
    return render(request, "course/register.html", {"form": form, "formset": formset})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("course:index")  # куда редирект после логина
    else:
        form = LoginForm()

    return render(request, "registration/login.html", {"form": form})

@login_required
def profile(request):
    return render(request, "course/profile.html")

@login_required
def dashboard(request):
    courses = StudentCourses.objects.filter(student=request.user)
    return render(request, "course/dashboard.html", {"courses": courses})

@login_required
def logout_view(request):
    logout(request)
    return redirect("course:index")