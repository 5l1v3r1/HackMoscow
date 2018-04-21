"""HackMoscow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from server.views import signup, team_info, create_team, signin
from server.views import signup, signin, hackaton_list, new_hackathon, change_hackathon
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup),
    path('teams/<int:team_id>', team_info),
	path('create_team/', create_team),
	path('signin/', signin)
    path('signin/', signin),
    path('new_hack/', new_hackathon),
    path('hack_list/', hackaton_list),
    path('change_hack_info/<int:id>', change_hackathon),
]
