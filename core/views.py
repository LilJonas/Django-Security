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
