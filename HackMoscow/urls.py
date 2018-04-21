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
from django.urls import path, include
from django.conf.urls.static import static
from server.views import team_info, create_team, hack_info, signup, signin, hackaton_list, new_hackathon, change_hackathon, add_user_to_hack, user_info, add_user_to_team
from ajax_select import urls as ajax_select_urls
from . import settings

urlpatterns = [
    path(r'^admin/lookups/', include(ajax_select_urls)),
    path('admin/', admin.site.urls),
    path('signup/', signup, name='sign_up'),
    path('teams/<int:team_id>', team_info, name='teams'),
	path('create_team/<int:hack_id>', create_team, name='create_team'),
    path('signin/', signin),
    path('lk/', user_info, name='profile'),
    path('new_hack/', new_hackathon),
    path('hack_list/', hackaton_list, name='hack_list'),
    path('change_hack_info/<int:id>', change_hackathon),
	path('hack_info/<int:hack_id>', hack_info, name='hack_info'),
	path('accounts/login/', signin),
	path('add_user_to_hack/<int:hack_id>/<int:user_id>', add_user_to_hack, name='add_user_to_hack'),
    path('add_user_to_team/<int:team_id>/<int:user_id>', add_user_to_team, name='add_user_to_team'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT,) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)