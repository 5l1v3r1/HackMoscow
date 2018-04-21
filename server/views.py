from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponse
from server.forms import SignUpForm, LoginForm, CreateTeamForm
from .models import Profile, Hackathon, Team, Skill
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, HttpResponseRedirect

from server.forms import SignUpForm, LoginForm, NewHackathonForm, ApplyToHack
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.forms.formsets import formset_factory
from django.forms.models import model_to_dict




@login_required
def user_info(request):
	if request.method == 'GET':
		user = Profile.objects.get(user_id=request.user.id)
		skills = user.skills.all()
		user_hack_rating = 0
		# endregion
		for hack in user.user.hackathon_set.order_by('id'):
			user_hack_rating += 10  # TODO: нормальный рейтинг
		diag = 'media/dia'+ str(user.id+1) + '.jpg'
		return render(request, 'profile.html', {'user': user, 'user_hack_rating': user_hack_rating, 'skills': skills,
												'diag':diag})


@login_required
# region Team
def team_info(request, team_id):
	'''provides information for team info page'''
	team = Team.objects.all().filter(id=team_id).first()
	if team != None:
		users = [user for user in team.users.all()]
		return render(request, 'team_info.html', {'team': team, 'users': users})
	else:
		return HttpResponse("403")


@login_required
def create_team(request, hack_id):
	'''creates team'''
	hack = get_object_or_404(Hackathon, id=hack_id)
	user = get_object_or_404(User, username=request.user.username)
	if request.method == 'POST':
		team_form = CreateTeamForm(request.POST)
		if team_form.is_valid():
			try:
				team = Team.objects.create()
				team.name = team_form.cleaned_data.get('name')
				team.hackathones.add(hack)
				team.save()
				team.users.add(user)
				team.save()
				print(user.id)

				return redirect('hack_info', hack_id=hack_id)

			except Exception as e:
				print(e)
				return HttpResponse("403")

	else:
		team_form = CreateTeamForm()
	return render(request, 'create_team.html', {'form': team_form, 'hack': hack, 'user': user})


# endregion

def hack_info(request, hack_id):
	hack = Hackathon.objects.get(id=hack_id)
	if hack != None:
		return render(request, 'hack_info.html', {'hack': hack})
	else:
		return HttpResponse("404")


# Create your views here.
def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST, request.FILES)
		if form.is_valid():
			user = form.save()
			prof = Profile(user=user, name=form.cleaned_data.get('first_name'),
						   surname=form.cleaned_data.get('last_name'), github=form.cleaned_data.get('github'),
						   vk=form.cleaned_data.get('vk'), facebook=form.cleaned_data.get('facebook'),
						   avatar=request.FILES['avatar'])
			prof.save()
			skills = request.POST.getlist('skills')
			skills = skills[0].split('|')
			if len(skills) != 2:
				for i in skills:
					if i.isdigit():
						skill = Skill.objects.get(id=int(i))
						prof.skills.add(skill)
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
					return HttpResponseRedirect('/lk')

				else:
					return HttpResponse("403")
			except Exception as e:
				print(e)
				return HttpResponse("403")
	else:
		form = LoginForm()
	return render(request, 'login.html', {'form': form})


'''View for new hackathons'''


@login_required
def new_hackathon(request):
	if request.method == 'POST':
		form = NewHackathonForm(request.POST)
		if form.is_valid():
			hackathon = form.save()
			hackathon.refresh_from_db()
			hackathon.save()
			tags = request.POST.getlist('tags')
			tags = tags[0].split('|')
			if len(tags) != 2:
				for i in tags:
					if i.isdigit():
						tag = Tag.objects.get(id=int(i))
						hackathon.tags.add(tag)
			return HttpResponse("Hackathon created!")
	else:
		form = NewHackathonForm()
	return render(request, 'new_hackathon.html', {'form': form})


def hackaton_list(request):
	hackatons = Hackathon.objects.all()

	return render(request, 'hackaton_list.html', {'hacks': hackatons})


'''change hackathon view'''


@login_required
def change_hackathon(request, id):
	hackaton = get_object_or_404(Hackathon, id=id)
	if request.method == 'POST':
		form = NewHackathonForm(request.POST)
		if form.is_valid():
			tmp = form.instance
			hackaton.date = tmp.date
			hackaton.name = tmp.name
			hackaton.description = tmp.description
			hackaton.duration = tmp.duration
			hackaton.max_members = tmp.max_members

			hackaton.save()

			return HttpResponse("Changes saved!")
	else:
		form = NewHackathonForm(instance=hackaton)
	return render(request, 'change_hack_info.html', {'form': form})


@login_required
# information about hack
def hack_info(request, hack_id):
	hack = get_object_or_404(Hackathon, id=hack_id)

	if request.user.username != "":
		user = get_object_or_404(User, username=request.user.username)
		applied_users = hack.users.filter(id=user.id)

		users_team_in_hack = None

		for team in user.team_set.order_by('id'):
			if team.hackathones.filter(id=hack.id).count() > 0:
				users_team_in_hack = team
				break

		return render(request, 'hack_info.html', {'hack': hack,
												  'user_id': user.id,
												  'is_user_applied': applied_users.count() != 0,
												  'user_has_team': users_team_in_hack is not None,
												  'users_team_in_hack': users_team_in_hack})
	else:
		return HttpResponse("Lol, who are you?")


@login_required
# adds user to hackathon
def add_user_to_hack(request, hack_id, user_id):
	hack = get_object_or_404(Hackathon, id=hack_id)
	user = get_object_or_404(User, id=user_id)
	hack.users.add(user)

	return HttpResponse("You are added!")
