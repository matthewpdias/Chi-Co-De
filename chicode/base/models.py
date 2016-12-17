from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.contrib import admin

class Project(models.Model):
    project_name = models.CharField(primary_key=True, max_length=64)
    project_description = models.TextField(blank=True, default='')
    tech_used = models.TextField(blank=True, default='')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, default='' ,related_name='project_owner')

    def __str__(self):
        return self.project_name

    def uses(self):
        return self.tech_used


class Upload(models.Model):
    filename = models.CharField(primary_key=True, max_length=64)
    description = models.CharField(null=True, max_length=256)
    upload = models.FileField(upload_to='uploads/')
    assoc_project = models.ForeignKey(Project, default='', related_name='associated_project')
    uploaded_by = models.ForeignKey(User, default='system', related_name='file_owner')

    def __str__(self):
        return self.filename

class Topic(models.Model):
    topic_name = models.CharField(primary_key=True, max_length=64)
    first = models.CharField(max_length=10000, default='This topic was created without an original post')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic_name

class TopicComment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    content = models.TextField(max_length=1000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return '{}@{}'.format(self.creator, self.created_at)

class ProjectComment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    content = models.TextField(max_length=1000)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return '{}@{}'.format(self.creator, self.created_at)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=20, null=True)
    skills = models.TextField(max_length=1000, null=True)
    about = models.TextField(max_length=1000)

    def __str__(self):
        return '{}`s profile'.format(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
