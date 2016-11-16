from django import forms
from base.models import Project, Comment, User


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        content = forms.CharField(max_length=200, help_text="enter your comment", required=True, widget=forms.Textarea)
        exclude = ('created_at', 'creator',)

    def cleaned():
        #TODO: add some logic to restrict user input

        return content


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
