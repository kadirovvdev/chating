from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import CustomUser


class RegisterView(View):
    def get(self, request):
        create_form = CreateUserForm()
        context = {'form': create_form}
        return render(request, 'users/register.html', context=context)

    def post(self, request):
        create_form = CreateUserForm(data=request.POST, files=request.FILES)
        if create_form.is_valid():
            create_form.save()
            print("Successfully created")
            return redirect('login')
        else:
            return render(request, 'users/register.html', context={'form': create_form})


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {'form': login_form}
        return render(request, 'users/login.html', context=context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            print("Successfully logged in")
            return redirect('inbox')
        else:
            context = {'form': login_form}
            print("Not Successfully logged in")
            return render(request, 'users/login.html', context=context)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        context = {
            'user': user
        }
        return render(request, 'users/profile.html', context=context)


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        return render(request, 'users/edit_profile.html', {'user': user})

    def post(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.pk)
        return render(request, 'users/edit_profile.html', {'user': user, 'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('landing-page')
