# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import poplib

###Test this view by using
###curl --data "webmail=k.raghuram&password=my_pass" http://127.0.0.1:8000/testoauth/
@csrf_exempt
def index(request):
	if request.method == "GET":
		return HttpResponse("Hi")
	elif request.method == "POST":
		#Get the data
		print "POST DATA :",request.POST
		webmail = request.POST['webmail']
		password = request.POST['password']

		#Get user object
		try:
			user = get_user_model().objects.get(webmail__contains=webmail)
		except get_user_model().DoesNotExist:
			return HttpResponse("Is this your first time bro?")

		#user will never be None (except get_user_model().DoesNotExist makes sure of that)
		#if user is not None:
		#Authenticate
		try:
			user = authenticate(request, webmail=user.webmail, mail_server=user.mail_server, password=password)
			if user is not None:
				login(request, user)
				# return HttpResponse(str(request.user.is_authenticated))
				return HttpResponse("Logged in bro")
				# Redirect to a success page.
				#...
			#Technically, it will never goto else, since
			#WebmailAuthenticationBackend.authenticate() returns None only when User DoesNotExist
			#And we made sure that user existed above(line 28)
			else:
				# Return an 'invalid login' error message.
				#...
				# return HttpResponse(str(request.user.is_authenticated))
				return HttpResponse("Authenticate failed bro")
		#When password is incorrect,
		#WebmailAuthenticationBackend.authenticate() returns below exception with message,
		#"-ERR Authentication failed."
		except poplib.error_proto as e:
			if e.message == "-ERR Authentication failed.":
				return HttpResponse("Password wrong bro")
			else:
				return HttpResponse(e.message)

	else:
		return HttpResponse("Neither GET nor POST bro")