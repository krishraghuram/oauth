from django import forms
from material import Layout

class LoginForm(forms.Form):
    webmail = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    layout = Layout('webmail', 'password')

#Todo
#class SignupForm