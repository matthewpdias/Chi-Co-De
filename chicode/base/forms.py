from django import forms
from base.models import Project, Comment, User, Profile


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        content = forms.CharField(max_length=200, help_text="enter your comment", required=True, widget=forms.Textarea)
        exclude = ('created_at', 'creator',)



class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']
        #username = forms.CharField(label='Username', max_length=20)
        #password = forms.CharField(label='password', max_length=32, widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ['user']
