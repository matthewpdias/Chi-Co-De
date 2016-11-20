from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from .models import Comment, Project, User
from .forms import CommentForm, UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django import forms

#from settings import *
def logout(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('/')

def index(request):
    return render(request, 'index.html')

def comment(request):
    return render(request, 'base.html')

def new_project(request):
    return render(request, 'base.html')

def login(request):
    if request.user.is_authenticated():
        return redirect('/home')
    return render(request, 'login.html')

def home(request):
    if request.user.is_authenticated():
        return render(request, 'home.html')
    return redirect('/login')

def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.about = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()

def register(request):
    if request.user.is_authenticated():
        return redirect('/home')
    if request.method == 'GET':
        uf = UserForm(prefix='user')
        upf = ProfileForm(prefix='userporfile')
        return render_to_response ('registration/register.html', dict(UserForm=uf, ProfileForm=upf), request)
    if request.method == 'POST':
        uf = UserForm(request.POST, prefix='user')
        upf = ProfileForm(request.POST, prefix='userprofile')
        if True:
            user = uf.save()
            userprofile = upf.save(commit=False)
            userprofile.user = user
            userprofile.save()
            return redirect('/home')
        return
