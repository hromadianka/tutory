from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Project, AddProject, Result, Feedback, CourseProject
from itertools import chain
import uuid

# Create your views here.

@login_required(login_url='/signin')
def index(request):
      user_object = User.objects.get(username=request.user.username)
      user_profile = Profile.objects.get(user=user_object)

      added_projects = AddProject.objects.filter(username=user_profile.user)
      Projects = []
      try:
          for project in added_projects:
              p = Project.objects.get(id=project.project_id)
              Projects.append(p)
      except:
          Projects = None
      
      try:
          user_projects = Project.objects.filter(user=user_profile.name)
      except:
          user_projects = None

      return render(request, 'index.html', {'user_profile': user_profile, 'Projects': Projects, 'user_projects': user_projects})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Ця пошта вже зайнята:( Спробуй увійти в акаунт')
                return redirect('/signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Цей нік вже зайнятий:( Спробуй інший')
                return redirect('/signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id, email=user.email, name=name)
                new_profile.save()
                return redirect('/')
        else:
            messages.info(request, 'Паролі не збігаються! Спробуй ще раз')
            return redirect('/signup')
        
    else:
        return render(request, 'signup.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Неправильна пошта або пароль')
            return redirect('/signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='/signin')
def logout(request):
    auth.logout(request)
    return redirect('/')

def profile1(request, pk):
    user_object = User.objects.get(username=pk)

    feedback = Feedback.objects.filter(student_username=user_object.username)

    user_profile = Profile.objects.get(user=user_object)
    context = {'user_profile': user_profile, 'feedback': feedback}
    return render (request, 'profile1.html', context)

def profile2(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)

    feedback = Feedback.objects.filter(business_username=user_object.username)

    context = {'user_profile': user_profile, 'feedback': feedback}
    return render (request, 'profile2.html', context)

@login_required(login_url='/signin')
def setting(request):

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
        
        user_profile.email = request.POST['email1']
        user_object.email = request.POST['email1']
        
        user_profile.description  = request.POST['description']
        user_profile.name  = request.POST['name']


        if request.POST['password_new'] != '':
            if request.POST['password_new'] != user_object.password:
                user_object.set_password(request.POST['password_new'])
        
        user_profile.save()
        user_object.save()
        return redirect('/setting')

    context = {'user': user_profile, 'user_object': user_object}
    return render(request, 'setting.html', context)

@login_required(login_url='/signin')
def create(request):
    if request.method == 'POST':
        user = Profile.objects.get(user=request.user.id)

        name = request.POST['name']
        description = request.POST['description']
        category = request.POST['category']

        project = Project.objects.create(name=name, description=description, category=category, user=user.name)
        project.save()

        return redirect('project', pk=project.id)

    return render(request, 'create.html')

@login_required(login_url='/signin')
def add(request):
    username = request.user.username
    project_id = request.GET.get('project_id')

    project = Project.objects.get(id=project_id)

    add_filter = AddProject.objects.filter(project_id=project_id, username=username).first()

    if add_filter == None:
        new_add = AddProject.objects.create(project_id=project_id, username=username)
        new_add.save()
        return redirect('project', pk=project_id)
    else:
        add_filter.delete()
        return redirect('project', pk=project_id)

def project(request, pk):
    project = Project.objects.get(id=pk)
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    add_filter = AddProject.objects.filter(project_id=project.id, username=request.user.username).first()
    if add_filter == None:
        button_text = 'Додати проєкт собі'
    else:
        button_text = 'Більше не беру участь'

    my_solutions = Result.objects.filter(username=request.user.username, project_id=project.id)

    creator = Project.objects.filter(id=pk, user=user_profile.name)
    results = Result.objects.filter(project_id=project.id)
    
    feedback = None

    for r in results:
        feedback = Feedback.objects.filter(result=r)

    if request.method == "POST":
        text = request.POST['text']
        student = request.POST['student']
        result_id = request.POST['result1']

        result1 = Result.objects.get(id=result_id)

        new_feedback = Feedback.objects.create(text=text, result=result1, business_username=request.user.username, student_username=student)
        project.save()

        return redirect('project', pk=project.id)
    
    context = {'project': project, 'button_text': button_text, 'add_filter': add_filter, 'my_solutions': my_solutions, 'creator': creator, 'results': results, 'feedback': feedback}
    return render(request, 'project.html', context)

@login_required(login_url='/signin')
def download(request, pk):
    user = request.user.username
    project = Project.objects.get(id=pk)

    if request.method == 'POST':
        if request.FILES.get('files') == None:
            name = request.POST['name']
            text = request.POST['text']
            result = Result.objects.create(name=name, text=text, username=user, project_id=project)
            result.save()

        if request.FILES.get('files') != None:
            name = request.POST['name']
            text = request.POST['text']
            files = request.FILES.get('files')
            result = Result.objects.create(name=name, text=text, files=files, username=user, project_id=project)
            result.save()

        return redirect('project', pk=project.id)
    return render(request, 'download.html')

@login_required(login_url='/signin')
def change(request, pk):
    project = Project.objects.get(id=pk)

    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        category = request.POST['category']

        project.name = name
        project.description = description
        project.category = category
        project.save()

        return redirect('project', pk=project.id)

    context = {'project': project}
    return render(request, 'change.html', context)

@login_required(login_url='/signin')
def delete(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('/')
    return render(request, 'delete.html')

def search(request):
    projects = None

    if request.method == 'POST':
        search = request.POST['search']
        projects1 = Project.objects.filter(name__icontains=search)
        projects2 = Project.objects.filter(description__icontains=search)
        projects3 = Project.objects.filter(category__icontains=search)
        projects = (projects1 | projects2 | projects3).distinct()

    context = {'projects': projects}
    return render(request, 'search.html', context)

@login_required(login_url='/signin')
def deleteaccount(request, pk):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    if request.method == 'POST':
        user_object.delete()
        user_profile.delete()
        return redirect('/')
    return render(request, 'deleteaccount.html')

def courses(request):
      return render(request, 'courses.html')

def webdev(request):
    webdev1_training = CourseProject.objects.filter(chapter='webdev1_training')
    webdev1_real = CourseProject.objects.filter(chapter='webdev1_real')
    webdev2_training = CourseProject.objects.filter(chapter='webdev2_training')
    webdev2_real = CourseProject.objects.filter(chapter='webdev2_real')
    webdev3_training = CourseProject.objects.filter(chapter='webdev3_training')
    webdev3_real = CourseProject.objects.filter(chapter='webdev3_real')
    webdev4_training = CourseProject.objects.filter(chapter='webdev4_training')
    webdev4_real = CourseProject.objects.filter(chapter='webdev4_real')
    
    context = {
        'webdev1_training': webdev1_training,
        'webdev1_real': webdev1_real,
        'webdev2_training': webdev2_training,
        'webdev2_real': webdev2_real,
        'webdev3_training': webdev3_training,
        'webdev3_real': webdev3_real,
        'webdev4_training': webdev4_training,
        'webdev4_real': webdev4_real,
    }
    return render(request, 'webdev.html', context)

def design(request):
      design1_training = CourseProject.objects.filter(chapter='design1_training')
      design1_real = CourseProject.objects.filter(chapter='design1_real')
      design2_training = CourseProject.objects.filter(chapter='design2_training')
      design2_real = CourseProject.objects.filter(chapter='design2_real')
      design3_training = CourseProject.objects.filter(chapter='design3_training')
      design3_real = CourseProject.objects.filter(chapter='design3_real')
      design4_training = CourseProject.objects.filter(chapter='design4_training')
      design4_real = CourseProject.objects.filter(chapter='design4_real')
      design5_training = CourseProject.objects.filter(chapter='design5_training')
      design5_real = CourseProject.objects.filter(chapter='design5_real')
      design6_training = CourseProject.objects.filter(chapter='design6_training')
      design6_real = CourseProject.objects.filter(chapter='design6_real')
      design7_training = CourseProject.objects.filter(chapter='design7_training')
      design7_real = CourseProject.objects.filter(chapter='design7_real')
      
      context = {
            'design1_training': design1_training,
            'design1_real': design1_real,
            'design2_training': design2_training,
            'design2_real': design2_real,
            'design3_training': design3_training,
            'design3_real': design3_real,
            'design4_training': design4_training,
            'design4_real': design4_real,
            'design5_training': design5_training,
            'design5_real': design5_real,
            'design6_training': design6_training,
            'design6_real': design6_real,
            'design7_training': design7_training,
            'design7_real': design7_real,
      }
      
      return render(request, 'design.html', context)

def projectmanagement(request):
      return render(request, 'projectmanagement.html')

def allprojects(request):
      Projects = Project.objects.all()
      return render(request, 'allprojects.html', {'Projects': Projects,})
