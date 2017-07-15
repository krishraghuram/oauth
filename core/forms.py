from django import forms
from material import Layout, Fieldset, Row
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
	webmail = forms.CharField(max_length=50)
	password = forms.CharField(widget=forms.PasswordInput)
	layout = Layout('webmail', 'password')
	
	def clean(self):
		try:
			cleaned_data = super(LoginForm, self).clean()
			cleaned_data['webmail'] = cleaned_data['webmail'].split("@")[0]
		except KeyError:
			raise ValidationError("Webmail cannot be empty")

class SignupForm(forms.Form):
	webmail = forms.CharField(max_length=50)
	password = forms.CharField(widget=forms.PasswordInput)    
	mail_server = forms.ChoiceField(choices=get_user_model().WEBMAIL_SERVERS)
	first_name = forms.CharField(max_length=50, required=False)
	last_name = forms.CharField(max_length=50, required=False)
	layout = Layout('webmail', 'password', 'mail_server', 
				Fieldset('Pesonal details',Row('first_name', 'last_name')))
	
	def clean(self):
		try:
			cleaned_data = super(SignupForm, self).clean()
			cleaned_data['webmail'] = cleaned_data['webmail'].split("@")[0]
		except KeyError:
			raise ValidationError("Webmail cannot be empty")