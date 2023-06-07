from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import subprocess
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from core.models import Guestbook
from django.utils import timezone
import configparser

config = configparser.ConfigParser()
config.read('core/static/core/navinfo.ini')

def index(request):
    context = { "navinfo": config['DEFAULT']['Index'] }
    return render(request, 'core/index.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {"form":form})

def profile(request):
    return render(request, 'user/profile.html', None)

@csrf_exempt
def changepass(request):
    context = { "navinfo": config['DEFAULT']['CSRF'] }
    if request.method == 'POST':
        password1 = request.POST.get('newpass1')
        password2 = request.POST.get('newpass2')
        if (password1 == password2):
            context = { "msg": 'Your new password is ' + password1,
                        "navinfo": config['DEFAULT']['CSRF']
            }
        else:
            context = { "msg": 'Passwords did not match.',
                        "navinfo": config['DEFAULT']['CSRF']
             }
        return render(request, 'user/changepass.html', context)
    return render(request, 'user/changepass.html', context)