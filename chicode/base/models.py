from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Project(models.Model):
    project_name = models.CharField(max_length=64)
    project_description = models.TextField(blank=True, default='')
    tech_used = models.TextField(blank=True, default='')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return self.project_name

    def uses(self):
        return self.tech_used

class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    content = models.TextField(max_length=10000)
