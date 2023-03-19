from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project, User, Profile
from .forms import ProjectForm, RegistrationForm, LoginForm
from django.db import connection
from django.contrib import messages

def index(request):
    return HttpResponse("Hello")
def projects(request):
    response = HttpResponse(f"<h1>Проекты</h1>")
    return response
def add_project(request):
    response = HttpResponse(f"<h1>Добавить проект</h1>")
    return response
def tables(request):
    cursor = connection.cursor()
    table_list = connection.introspection.get_table_list(cursor)
    return HttpResponse(table_list)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data['user_type']
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            profile = user.profile
            profile.user_type = user_type
            profile.name = name
            profile.last_name = last_name
            profile.save()
            if user_type == 'STUDENT':
                student_group = Group.objects.get(name='Студенты')
                student_group.user_set.add(user)
            elif user_type == 'INVESTOR':
                investor_group = Group.objects.get(name='Инвесторы')
                investor_group.user_set.add(user)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

@login_required
def personal_cabinet(request):
    username = request.user.username
    projects = Project.objects.filter(created_by=request.user)
    return render(request, 'personal_cabinet.html', {'username': username, 'projects': projects})

@login_required
def create_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, 'Project created successfully!')
            return redirect('personal_cabinet')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         user_type = instance.profile.user_type
#         if user_type == 'STUDENT':
#             Student.objects.create(user=instance)
#         elif user_type == 'INVESTOR':
#             Investor.objects.create(user=instance)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            # Получаем email и пароль из формы
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Аутентифицируем пользователя
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Устанавливаем сессию и редиректим на нужную страницу
                login(request, user)
                if user.profile.user_type == 'INVESTOR':
                    return redirect('investor_cabinet')
                else:
                    return redirect('personal_cabinet')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def investor_cabinet(request):
    order_by = request.GET.get('order_by', 'title')
    projects = Project.objects.order_by(order_by)
    return render(request, 'investor_cabinet.html', {'projects': projects})

