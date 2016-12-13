from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from .models import *
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django import forms

def add_topic(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            new_topic = Topic()
            form.scrub()
            new_topic.topic_name = form.cleaned_data['topic_name']
            new_topic.first = form.cleaned_data['first']
            new_topic.save()
            url = '/viewtopic/' + new_topic.topic_name + '/'
            return redirect(url)
    else:
        form = NewTopicForm()
        return render(request, 'new_topic.html', {'form' : form })

def add_project(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        if form.is_valid():
            form.scrub()
            new_project = Project()
            new_project.project_name = form.cleaned_data['project_name']
            new_project.project_description = form.cleaned_data['project_description']
            new_project.tech_used = form.cleaned_data['tech_used']
            new_project.owner = request.user
            new_project.save()
            url = '/viewproject/' + new_project.project_name + '/'
            return redirect(url)
    else:
        form = NewProjectForm()
        return render(request, 'new_project.html', {'form' : form })

def index(request):
    return render(request, 'index.html')

def comment(request):
    return render(request, 'base.html')

def new_project(request):
    return render(request, 'base.html')

def home(request):
    if request.user.is_authenticated():
        projects = Project.objects.filter(owner=request.user).all()
        #get the last TopicComments the user has made, sorted by creation.. May limit to less eventually
        Tcomments = TopicComment.objects.filter(creator=request.user).all().order_by('created_at')#[:10]
        mytopics = set()
        #store recent topics those commets relate to in a set to eliminate repeats
        for comment in Tcomments:
            mytopics.add(comment.topic)
        #store the most recent comment for each recent topic for dashboard digest
        topic_digest = dict.fromkeys(mytopics, 'no comments')

        for topic in topic_digest:
            topic_digest[topic] = TopicComment.objects.filter(topic=topic).order_by('created_at').reverse()[0]

        return render(request, 'home.html', {'projects'  : projects, 'topic_digest' : topic_digest})
    return redirect('/login')

def edit_profile(request, user):
    if request.user != User.objects.filter(username=user).first():
        return redirect('/home')
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            profile = get_object_or_404(Profile, user=request.user)
            #major skills about
            profile.major = form.cleaned_data['major']
            profile.skills = form.cleaned_data['skills']
            profile.about = form.cleaned_data['about']
            profile.save(update_fields=['major','skills','about'])
            return redirect('/home')
    else:
        form = EditProfileForm()
        return render(request, 'edit_profile.html', {'form': form})

def upload_file(request, project):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Upload(up_file=request.FILES['up_file'])
            up_description = form.cleaned_data['up_description']
            instance.assoc_project = Project.objects.filter(project_name=project).first()
            instance.save()
            return redirect('/home')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def view_profile(request, username):
    userobj =  User.objects.filter(username=username).first()
    if not userobj:
        return render(request, 'profile_404.html')

    profile = Profile.objects.filter(user=userobj).first()
    projects = Project.objects.filter(owner=userobj).all()
    if userobj == request.user:
        myprofile = True
    else:
        myprofile = False
    return render(request, 'profile.html', {'user': username, 'profile': profile, 'projects': projects, 'myprofile' : myprofile})

def view_topic(request, topicname):
    if not request.user.is_authenticated():
        return redirect('/login')

    topic = Topic.objects.filter(topic_name=topicname).first()
    comments = TopicComment.objects.filter(topic=topic).all()
    form = TopicCommentForm()
    source = request.path

    if request.method == 'POST':
        form = TopicCommentForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            new_comment = TopicComment()
            new_comment.creator = request.user
            new_comment.content = form.cleaned_data['content']
            new_comment.topic = topic
            new_comment.save()
            return redirect(request.path)
    else:
        return render(request, 'topic.html', {'topic': topic, 'comments': comments, 'form': form })

def view_project(request, projectname):
    if not request.user.is_authenticated():
        return redirect('/login')

    project = Project.objects.filter(project_name=projectname).first()
    comments = ProjectComment.objects.filter(project=projectname).all()
    form = ProjectCommentForm()
    source = request.path
    if request.method == 'POST':
        form = ProjectCommentForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            new_comment = ProjectComment()
            new_comment.creator = request.user
            new_comment.content = form.cleaned_data['content']
            new_comment.project = project
            new_comment.save()
            return redirect(request.path)
    else:
        return render(request, 'project.html', {'project': project, 'comments': comments, 'form': form, 'url': source})

def project_index(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    project_list = Project.objects.all()
    return render(request, 'project_index.html', {'projects': project_list})

def topic_index(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    topic_list = Topic.objects.all()
    return render(request, 'topic_index.html', {'topics': topic_list})

def my_login(request):
    if request.user.is_authenticated():
        return redirect('/home')
    if request.method == 'GET':
        logform = LogForm()
        return render(request, 'registration/login.html', {'form' : logform})
    if request.method == 'POST':
        form = LogForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home')
            else:
                logform = LogForm()
                message = 'invalid credentials, try again'
        else:
            logform = LogForm()
            message = 'form invalid'
        return render(request, 'registration/login.html', {'form' : logform, 'message': message} )


def my_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('/login')


def my_register(request):
    if request.user.is_authenticated():
        return redirect(request.post, '/home')
    if request.method == 'GET':
        form = RegisterForm
        return render(request, 'registration/register.html', {'form' : RegisterForm})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.check_pass():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                email = form.cleaned_data['email']
                try:
                    new_user = User.objects.create_user(username, email, password)
                except:
                    message = 'username already taken, please try a new one'
                    return render(request, 'registration/register.html', {'form' : RegisterForm, 'message': message})
                login(request, new_user)
                return redirect('/home')
            else:
                message = 'passwords must match'
                return render(request, 'registration/register.html', {'form' : RegisterForm, 'message': message})
        else:
            message = 'invalid form contents'
            return render(request, 'registration/register.html', {'form' : RegisterForm, 'message': message})
