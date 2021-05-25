from django.db import reset_queries
from django.shortcuts import redirect, render
from django.views.generic.base import View
from .forms import *
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class RegistrationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main:home')
        else:
            form = RegistrationForm()

            return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('main:home')
        else:
            form = RegistrationForm(request.POST or None)

            if form.is_valid():
                user = form.save()
                raw_password = form.cleaned_data.get('password1')

                user = authenticate(username = user.username, password=raw_password)

                login(request, user)

                return redirect('main:home')
        
        return render(request, 'accounts/register.html', {'form': form})


class LoginUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main:home')
        else:
            return render(request, 'accounts/login.html')

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('main:home')
        else:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    
                    return redirect('main:home')
                else:
                    return render(request, 'accounts/login.html', {'error', 'Your account has been disabled.'})
            else:
                return render(request, 'accounts/login.html', {'error': 'Invalid Username or Password. Try Again.'})


class LogoutUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)

            return redirect('accounts:login')
        else:
            return redirect('accounts:login')
