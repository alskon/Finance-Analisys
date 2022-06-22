from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


class LoginUser(View):

    def get(self, request):
        return render(request, 'auth/login.html', {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('start')
        else:
            messages.error(request, 'Login error!')
            return redirect('login')


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('start')


class RegisterUser(View):
    pass
