"""chicode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib import auth
from django.contrib.auth import views as auth_views

from base import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^comment/[0-9]+/$', views.comment, name="comment"),
    url(r'^newproject/[0-9]+/$', views.new_project, name='new_project'),
    url(r'^login/$', views.my_login, name='login'),
    url(r'^logout/$', views.my_logout, name='logout'),
    url(r'^register/', views.my_register, name='register'),
    url(r'^viewprofile/([A-Z]+[a-z]*[0-9]*|[a-z]+[A-Z]*[0-9]*|[0-9]+[a-z]*[A-Z]*)', views.view_profile, name="view_profile"),
    url(r'^home/$', views.home, name='home'),
]
