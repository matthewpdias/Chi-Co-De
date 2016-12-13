from django import forms
from base.models import *
import re

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['up_name', 'up_description', 'up_file']

class NewTopicForm(forms.Form):
    topic_name = forms.CharField(max_length = 64, required=True)
    first = forms.CharField(max_length=1000, widget=forms.Textarea, label='Start the disussion')

    def scrub(self):
        self.cleaned_data['topic_name'] = self.cleaned_data['topic_name'].replace(' ','')

        self.cleaned_data['topic_name'] = re.sub('[^a-zA-Z0-9]+','',self.cleaned_data['topic_name'])

class NewProjectForm(forms.Form):
    project_name = forms.CharField(max_length=64)
    project_description = forms.CharField(max_length=10000, widget=forms.Textarea)
    tech_used = forms.CharField(max_length=1000, widget=forms.Textarea)

    def scrub(self):
        self.cleaned_data['project_name'] = self.cleaned_data['project_name'].replace(' ','')

        self.cleaned_data['project_name'] = re.sub('[^a-zA-Z0-9]+','',self.cleaned_data['project_name'])

class EditProfileForm(forms.Form):
    major = forms.CharField(max_length=10)
    skills = forms.CharField(max_length=1000, widget=forms.Textarea)
    about = forms.CharField(max_length=1000, label='About you', widget=forms.Textarea)


class ProjectCommentForm(forms.Form):
    content = forms.CharField(max_length=200, help_text="enter your comment", required=True, widget=forms.Textarea)
    exclude = ('created_at', 'creator', 'project')

class TopicCommentForm(forms.Form):
    content = forms.CharField(max_length=200, help_text="enter your comment", required=True, widget=forms.Textarea)
    exclude = ('created_at', 'creator', 'project')


class LogForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.CharField(label='Email Address', max_length=200)
    password1 = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm', max_length=32, widget=forms.PasswordInput)


    def check_pass(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            return False
        return True
