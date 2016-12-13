from django.contrib import admin

from .models import *

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(ProjectComment)
admin.site.register(TopicComment)
admin.site.register(Topic)
# Register your models here.
