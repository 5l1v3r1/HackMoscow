from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponse
from server.forms import SignUpForm, LoginForm
from django.contrib.auth.models import User
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
    