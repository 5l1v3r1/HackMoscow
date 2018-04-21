from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from server.forms import SignUpForm, LoginForm, NewHackathonForm
from django.contrib.auth.models import User
from server.models import Hackathon
from django.forms.models import model_to_dict


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



'''View for new hackathons'''
def new_hackathon(request):
    if request.method == 'POST':
        form = NewHackathonForm(request.POST)
        if form.is_valid():
            hackathon = form.save()
            hackathon.refresh_from_db()
            hackathon.save()

            return HttpResponse("Hackathon created!")
    else:
        form = NewHackathonForm()
    return render(request, 'new_hackathon.html', {'form': form})

def hackaton_list(request):
    hackatons = Hackathon.objects.all()
    return render(request, 'hackaton_list.html', {'hacks':hackatons})


def hackathon_page(request, id):
    try:
        hack = Hackathon.objects.get(id=id)
        return render(request, 'hackaton', {'hack':hack} )
    except:
        return HttpResponse("404")


'''change hackathon view'''
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




    

