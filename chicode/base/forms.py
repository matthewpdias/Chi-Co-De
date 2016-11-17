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

    class Meta():
        model = User
        fields = "__all__"
        username = forms.CharField(label='Username', max_length=20)
        password1 = forms.CharField(label='password', max_length=32, widget=forms.PasswordInput)
        password2 = forms.CharField(label='confirm password', max_length=32, widget=forms.PasswordInput)

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')
