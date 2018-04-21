from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponse
from server.forms import SignUpForm, LoginForm, CreateTeamForm
from .models import Profile, Hackathon, Team
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory


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

#region Team
def team_info(request, team_id):
	'''provides information for team info page'''
	team = Team.objects.all().filter(id = team_id).first()
	if team != None:
		users = [user for user in team.users.all()]
		return render(request, 'team_info.html', {'team':team, 'users': users})
	else:
		return HttpResponse("403")


def create_team(request):
	'''creates team'''
	if request.method == 'POST':
		team_form = CreateTeamForm(request.POST)
		if team_form.is_valid():
			try:
				team = Team.objects.create()
				team.name = team_form.cleaned_data.get('name')
				for i in range(3):
					form_username = team_form.cleaned_data.get('participant' + (str)(i+1))
					user = User.objects.all().filter(username=form_username).first()
					if user != None:
						team.users.add(user)
					else:
						return HttpResponse("403")
				team.save()
			except Exception as e:
				print(e)
				return HttpResponse("403")

	else:
		team_form = CreateTeamForm()
	return render(request, 'create_team.html', {'form':team_form})

#endregion


# Create your views here.
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
			return HttpResponse("You did it!!!!")
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})


def signin(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			try:
				username = form.cleaned_data.get('username')
				raw_password = form.cleaned_data.get('password')
				user = authenticate(username=username, password=raw_password)
				if user:
					login(request, user)
					return HttpResponse("200")
				else:
					return HttpResponse("403")
			except Exception as e:
				print(e)
				return HttpResponse("403")
	else:
		form = LoginForm()
	return render(request, 'login.html', {'form': form})
