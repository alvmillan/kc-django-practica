from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout
from django.views import View

from users.forms import LoginForm, SignUpForm


class LoginView(View):

    def render_template_with_form(self, request, form):
        context = {'form': form}
        return render(request, 'users/login.html', context)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        form = LoginForm()
        return self.render_template_with_form(request, form)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('usr')
            password = form.cleaned_data.get('pwd')
            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, 'Usuario/contraseña incorrectos')
            else:
                django_login(request, user)
                url = request.GET.get('next', 'home')
                return redirect(url)

        return self.render_template_with_form(request, form)


class LogoutView(View):

    def get(self, request):
        django_logout(request)
        return redirect('login')


class SignUpView(View):

    def get(self, request):
        form = SignUpForm()
        context = {'form': form}
        return render(request, 'users/sign_up.html', context)

    def post(self, request):
        user = User()
        form = SignUpForm(request.POST, instance=user)
        if form.is_valid():
            new_user = User.objects.create_user(form.cleaned_data.get('username'), None, form.cleaned_data.get('password'))
            messages.success(request, 'Account created correctly with ID {0}'.format(new_user.pk))
            form = SignUpForm
        context = {'form': form}
        return render(request, 'users/sign_up.html', context)
