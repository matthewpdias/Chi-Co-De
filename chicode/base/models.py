from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
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
    content = models.TextField(max_length=1000)

class Skill(models.Model):
    name = models.CharField(max_length=64)

class Major(models.Model):
    name = models.CharField(max_length=10)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, null=True)
    skills = models.ForeignKey(Skill, null=True)
    about = models.TextField(max_length=1000)
    project = models.ForeignKey(Project, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
