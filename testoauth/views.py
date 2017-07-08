# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

#################################################################
###TEST LOGIN VIEW
#################################################################
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth import get_user_model
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# import poplib
# ###Test this view by using
# ###curl --data "webmail=k.raghuram&password=my_pass" http://127.0.0.1:8000/testoauth/
# @csrf_exempt
# def index(request):
# 	if request.method == "GET":
# 		return HttpResponse("Hi")
# 	elif request.method == "POST":
# 		#Get the data
# 		print "POST DATA :",request.POST
# 		webmail = request.POST['webmail']
# 		password = request.POST['password']
# 		#Get user object
# 		try:
# 			user = get_user_model().objects.get(webmail__contains=webmail)
# 		except get_user_model().DoesNotExist:
# 			return HttpResponse("Is this your first time bro?")
# 		#user will never be None (except get_user_model().DoesNotExist makes sure of that)
# 		#if user is not None:
# 		#Authenticate
# 		try:
# 			user = authenticate(request, webmail=user.webmail, mail_server=user.mail_server, password=password)
# 			if user is not None:
# 				login(request, user)
# 				# return HttpResponse(str(request.user.is_authenticated))
# 				return HttpResponse("Logged in bro")
# 				# Redirect to a success page.
# 				#...
# 			#Technically, it will never goto else, since
# 			#WebmailAuthenticationBackend.authenticate() returns None only when User DoesNotExist
# 			#And we made sure that user existed above(line 28)
# 			else:
# 				# Return an 'invalid login' error message.
# 				#...
# 				# return HttpResponse(str(request.user.is_authenticated))
# 				return HttpResponse("Authenticate failed bro")
# 		#When password is incorrect,
# 		#WebmailAuthenticationBackend.authenticate() returns below exception with message,
# 		#"-ERR Authentication failed."
# 		except poplib.error_proto as e:
# 			if e.message == "-ERR Authentication failed.":
# 				return HttpResponse("Password wrong bro")
# 			else:
# 				return HttpResponse(e.message)
# 	else:
# 		return HttpResponse("Neither GET nor POST bro")
#################################################################
#################################################################
#################################################################



#################################################################
###FUNCTION BASED LOGIN VIEW
#################################################################
# import poplib
# from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.auth import get_user_model, authenticate, login
# from django.contrib import messages
# from django.urls import reverse
# from django.shortcuts import render
# from django.views import View
# from . forms import LoginForm
# def loginview(request):
# 	# if this is a POST request we need to process the form data
# 	if request.method == 'POST':
# 		# create a form instance and populate it with data from the request:
# 		form = LoginForm(request.POST)
# 		# check whether it's valid:
# 		if form.is_valid():
# 			# Get the data
# 			webmail = form.cleaned_data['webmail']
# 			password = form.cleaned_data['password']
# 			#Get user object
# 			try:
# 				user = get_user_model().objects.get(webmail__contains=webmail)
# 			except get_user_model().DoesNotExist: #New User
# 				#Redirect to Sign Up Page
# 				return HttpResponse("Is this your first time?")
# 				# return HttpResponseRedirect("Sign Up URL")
# 			#Authenticate
# 			try:
# 				user = authenticate(request, webmail=user.webmail, mail_server=user.mail_server, password=password)
# 				if user is not None:
# 					login(request, user)
# 					# Redirect to a success page.
# 					return HttpResponse("Logged in")
# 					# return HttpResponseRedirect("Wherever user needs to go after login. Possibly back to the the client who sent him here for oauth.")
# 				else:
# 					messages.error(request, "Authentication Failed. Try again later.")
# 					return HttpResponseRedirect(reverse('login'))
# 			#When password is incorrect,
# 			#WebmailAuthenticationBackend.authenticate() returns below exception with message,
# 			#"-ERR Authentication failed."
# 			except poplib.error_proto as e:
# 				if e.message == "-ERR Authentication failed.":
# 					messages.error(request, "Username or Password Incorrect")
# 					return HttpResponseRedirect(reverse('login'))
# 				else:
# 					messages.error(request, e.message)
# 					return HttpResponseRedirect(reverse('login'))
# 	# if a GET (or any other method) we'll create a blank form
# 	else:
# 		form = LoginForm()
# 	return render(request, 'testoauth/login.html', {'form':form})
#################################################################
#################################################################
#################################################################



###CLASS BASED LOGIN VIEW
import poplib
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render
from django.views import View
from . forms import LoginForm

class LoginView(View):
	form_class = LoginForm
	initial = {}
	template_name = 'testoauth/login.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class(initial=self.initial)
		return render(request, self.template_name, {'form':form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			# Get the data
			webmail = form.cleaned_data['webmail']
			password = form.cleaned_data['password']

			#Get user object
			try:
				user = get_user_model().objects.get(webmail__contains=webmail)
			except get_user_model().DoesNotExist: #New User
				#Redirect to Sign Up Page
				# return HttpResponseRedirect("Sign Up URL")
				str = '''
				<html><body style="text-align:center"><h1>
				<br/><br/><br/><br/><br/><br/><br/><br/>
				Is this your first time?
				</h1></body></html>
				'''
				return HttpResponse(str)
			
			#Authenticate
			try:
				user = authenticate(request, webmail=user.webmail, mail_server=user.mail_server, password=password)
				if user is not None:
					login(request, user)
					# Redirect to a success page.
					# return HttpResponseRedirect("Wherever user needs to go after login. Possibly back to the the client who sent him here for oauth.")
					str = '''
					<html><body style="text-align:center"><h1>
					<br/><br/><br/><br/><br/><br/><br/><br/>
					Logged in.	
					</h1></body></html>
					'''
					return HttpResponse(str)
				else:
					messages.error(request, "Authentication Failed. Try again later.")
					return HttpResponseRedirect(reverse('login'))
			#When password is incorrect,
			#WebmailAuthenticationBackend.authenticate() returns below exception with message,
			#"-ERR Authentication failed."
			except poplib.error_proto as e:
				if e.message == "-ERR Authentication failed.":
					messages.error(request, "Username or Password Incorrect")
					return HttpResponseRedirect(reverse('login'))
				else:
					messages.error(request, e.message)
					return HttpResponseRedirect(reverse('login'))
		else: # If form is not valid
			# Render the form, along with the errors generated by is_valid()
			return render(request, 'testoauth/login.html', {'form':form})


