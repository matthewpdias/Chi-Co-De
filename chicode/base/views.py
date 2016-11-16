from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
#from django.core.context_processors import csrf
from .models import Comment, Project, User
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
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

def register(request):
    context = RequestContext(request)

    successful = False

    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST)

        if register_form.is_valid():
            user = register_form.save()
            user.set_password(user.password)
            user.save()

            successful = True

        else:
            print (register_form.errors)

    else:
        register_form = RegisterForm()

    return render_to_response('register.html',{'register_form' : register_form, 'successful' : successful}, context)
