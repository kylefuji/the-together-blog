from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm

def index(request):
    return render(request, 'home/index.html', {'sliderRange':range(9)})

def login_redirect(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(index)
        return render(request, 'home/login.html', {'form':form})
    # check if user is still logged in then redirect to home page:
    if request.user.is_authenticated:
        return redirect(index)
    
    form = AuthenticationForm()
    return render(request, 'home/login.html', {'form':form})

def logout_redirect(request):
    logout(request)
    return redirect(index)