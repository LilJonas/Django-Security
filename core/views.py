from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django import forms
from django.contrib.auth.forms import UserCreationForm
import subprocess
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.models import *
from django.utils import timezone
import configparser
from django.db import connection

config = configparser.ConfigParser()
config.read('core/static/core/navinfo.ini', encoding='utf-8')

def index(request):
    context = { "navinfo": config['DEFAULT']['Index'] }
    return render(request, 'core/index.html', context)

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

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

@login_required
def profile(request):
    return render(request, 'user/profile.html', None)

# @csrf_exempt
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

def testconn(request):
    context = { "navinfo": config['DEFAULT']['CommandExec'] }
    if request.method == 'POST':
        webAddr = request.POST.get('serveraddr')
        procOut = subprocess.check_output('powershell.exe Test-Connection ' + webAddr, shell=True)
        context = { 
            "stdout": procOut.decode(),
            "navinfo": config['DEFAULT']['CommandExec']
        }
        return render(request, 'utils/testconn.html', context)
    return render(request, 'utils/testconn.html', context)

def filerunner(request):
    if request.method == 'GET':
        file = request.GET.get('file')
        if(file):
            procOut = subprocess.check_output(['python', file], shell=True)
            context = {
                "stdout": procOut.decode(),
                "file1": "fibonacci.py",
                "file2": "version.py",
                # "file3": "name.py",
                "navinfo": config['DEFAULT']['FileInclusion']
            }
            return render(request, 'utils/filerunner.html', context)
    context = {
        "file1": "fibonacci.py",
        "file2": "version.py",
        # "file3": "name.py",
        "navinfo": config['DEFAULT']['FileInclusion']
    }
    return render(request, 'utils/filerunner.html', context)

def userlookup(request):
    context = { "navinfo": config['DEFAULT']['SQLi'] }
    if request.method == 'POST':
        uname = request.POST.get('uname')
        query = User.objects.raw('SELECT * from "auth_user" WHERE "auth_user"."username" = "' + uname + '"')
        context = { "stdout": query,
                    "navinfo": config['DEFAULT']['SQLi']
        }
        return render(request, 'utils/userlookup.html', context)
    return render(request, 'utils/userlookup.html', context)

def guestbook(request):
    if request.method == 'POST':
        ubook = request.POST.get('ubook')
        desc = request.POST.get('desc')
        gbook = Product(name=ubook, description=desc)
        gbook.save()
    posts = Product.objects.all()
    if posts:
        context= {"posts": posts,
                  "navinfo": config['DEFAULT']['XSSs']
        }
    else:
        context= { "navinfo": config['DEFAULT']['XSSs'] }
    return render(request, 'utils/guestbook.html', context)

# def search_users(request):
#     context = { "navinfo": config['DEFAULT']['SQLi'] }
#     if request.method == 'POST':
#         query = request.POST.get('query')

#         # Vulnerable code: Concatenating user input directly into the SQL query
#         sql = User.objects.raw('SELECT * from "core_user" WHERE "username"= "' + query +'"')
        
#         # Executing the SQL query
#         # with connection.cursor() as cursor:
#         #     cursor.execute(sql)
#         #     users = cursor.fetchall()
#         context = { "stdout": sql,
#                     "navinfo": config['DEFAULT']['SQLi']
#         }
#         return render(request, 'utils/search_users.html', context)
#     return render(request, 'utils/search_users.html', context)


# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']

#         if password != confirm_password:
#             return render(request, 'registration/register.html', {'error': 'Passwords do not match.'})
        
#         # Create a new User instance without hashing the password
#         user = User(username=username, password=password)
#         user.save()

#         return redirect('login')

#     return render(request, 'registration/register.html')

# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
        
#         try:
#             # Retrieve the User instance based on the provided username
#             user = User.objects.get(username=username)
            
#             # Check if the password matches (plaintext comparison)
#             if user.password == password:
#                 request.session['username'] = username
#                 return redirect('profile')
#             else:
#                 return render(request, 'registration/login.html', {'error': 'Invalid credentials.'})
#         except User.DoesNotExist:
#             return render(request, 'registration/login.html', {'error': 'User does not exist.'})

#     return render(request, 'registration/login.html')

# @login_required
# def profile(request):
#     username = None
#     if 'username' in request.session:
#         username = request.session['username']
#     return render(request, 'user/profile.html', {'username': username})