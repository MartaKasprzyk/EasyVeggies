from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages


class RegisterUserView(View):

    def get(self, request):
        return render(request, 'registration.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')

        try:
            if password != password_repeat:
                return render(request, 'registration.html', {'error': 'Passwords are different! '
                                                                      'Please try again.'})

            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()

            messages.info(request, "User registered successfully.")
            return redirect("base")

        except IntegrityError:
            return render(request, 'registration.html', {'error': 'This username is already taken. '
                                                                  'Please try again.'})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        url = request.GET.get('next', 'base')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(url)
        return render(request, 'login.html', {'error': 'Login unsuccessful. Please try again.'})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('base')
