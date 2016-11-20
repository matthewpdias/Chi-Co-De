from django.contrib import admin

from .models import Comment
from .models import User
from .models import Profile

admin.site.register(Comment)
admin.site.register(Profile)
# Register your models here.
