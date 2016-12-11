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
    owner = models.ForeignKey(User, related_name='project_owner')

    def __str__(self):
        return self.project_name

    def uses(self):
        return self.tech_used

class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    content = models.TextField(max_length=1000)

    def __str__(self):
        return '{}@{}'.format(self.creator, self.created_at)

class Skill(models.Model):
    description = models.CharField(max_length=64)

    def __str__(self):
        return self.description

class Major(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, null=True)
    skills = models.ManyToManyField(Skill)
    about = models.TextField(max_length=1000)
    projects = models.ManyToManyField(Project)

    def __str__(self):
        return '{}`s profile'.format(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
