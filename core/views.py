import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View


class RegisterView(View):
    form_class = UserCreationForm
    template_name = 'core/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email_pattern = re.compile('^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$')
            if email_pattern.match(request.POST['email']) is not None:
                user = User.objects.create_user(username=request.POST['username'],
                                         password=request.POST['password2'],
                                         email=request.POST['email'])
                login(request, user)
                return redirect('/')
            else:
                error = 'Invalid type of email. Enter valid email'
                return render(request, self.template_name, {'form': form, 'custom_error': error})
        else:
            return render(request, self.template_name, {'form': form})


class LoginView(View):
    form_class = AuthenticationForm
    template_name = 'core/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print(user)
                login(request, user)
                return redirect('/')
                # return render(request, 'core/index.html')
            else:
                return HttpResponse('<h1> User not found</h1>')
        else:
            return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/login')
