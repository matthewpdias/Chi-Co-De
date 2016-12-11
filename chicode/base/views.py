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

def index(request):
    return render(request, 'index.html')

def comment(request):
    return render(request, 'base.html')

def new_project(request):
    return render(request, 'base.html')

def home(request):
    if request.user.is_authenticated():
        return render(request, 'home.html')
    return redirect('/login')

def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.about = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()

def view_profile(request, username):
    userobj =  User.objects.filter(username=username).first()
    if not userobj:
        return render(request, 'profile_404.html')

    profile = Profile.objects.filter(user=userobj).first()
    skills = profile.skills.all()
    return render(request, 'profile.html', {'user': username, 'profile': profile, 'skills': skills})


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
