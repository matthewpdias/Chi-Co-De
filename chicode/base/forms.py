from django import forms
from base.models import Project, Comment, User, Profile


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        content = forms.CharField(max_length=200, help_text="enter your comment", required=True, widget=forms.Textarea)
        exclude = ('created_at', 'creator',)


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
