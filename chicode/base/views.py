from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from .models import Comment, Project, User
from .forms import CommentForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import redirect

#from settings import *

def index(request):
    return render(request, 'index.html')

def comment(request):
    return render(request, 'base.html')

def new_project(request):
    return render(request, 'base.html')

def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.about = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()

def register(request):
    if request.method == 'GET':
        return render(request, 'registration/register.html')
    if request.method == 'POST':
        form = RegisterForm(data = request.POST)
        if form.is_valid():
            user = form.save(False)
            user.set_password(user.password)
            user.save()
            user = authenticate(username=User.username, password=request.POST['password1'])
            login(request, user)

        return redirect('/home')
