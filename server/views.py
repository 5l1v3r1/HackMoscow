from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from server.forms import SignUpForm, LoginForm
from .models import Profile, Hackathon

def user_info(request):
	if request.method == 'GET':
		user = Profile.objects.get(pk=id)
		return render(request, 'profile.html', )

def all_hackathones(request):
	hacks = Hackathon.objects.all()
	return render(request, 'hacks.html', {'hacks': hacks})

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return "You did it!!!!"
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})


def signin(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user = form.save()

	else:
		form = LoginForm()
	return render(request, 'login.html', {'form': form})