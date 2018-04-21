from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from django.forms.formsets import BaseFormSet
from django.forms import ModelForm
from .models import Hackathon


class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=True)
	last_name = forms.CharField(max_length=30, required=True)
	github = forms.CharField(max_length=100, required=True)
	vk = forms.CharField(max_length=100, required=True)
	facebook = forms.CharField(max_length=100, required=True)
	email = forms.EmailField(max_length=254)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'github', 'vk', 'facebook')


class LoginForm(forms.Form):
	username = forms.CharField(max_length=254, required=True)
	password = forms.CharField(widget=forms.PasswordInput())

class ApplyToHack(ModelForm):
	hack = forms.HiddenInput
	class Meta:
		model = User
		fields = ('id','username', 'first_name', 'last_name',
				  'email')






'''form for new hackathon'''


class NewHackathonForm(forms.ModelForm):
	class Meta:
		model = Hackathon
		fields = ['name', 'description', 'max_members', 'date', 'duration']

	def __init__(self, *args, **kwargs):
		super(NewHackathonForm, self).__init__(*args, **kwargs)
		self.fields['date'].widget = forms.DateInput(format='%d/%m/%y')

		username = forms.CharField(max_length=254, required=True)
		password = forms.CharField(widget=forms.PasswordInput())


class CreateTeamForm(forms.Form):
	name = forms.CharField(max_length=100, required=True)
	participant1 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
		'placeholder': 'username',
	}), required=True)
	participant2 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
		'placeholder': 'username',
	}), required=True)
	participant3 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
		'placeholder': 'username',
	}), required=True)
