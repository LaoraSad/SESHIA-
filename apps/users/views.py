from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.users.forms.login_form import LoginForm
from apps.users.forms.profile_form import ProfileForm
from apps.users.forms.register_form import RegisterForm


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "auth/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            return render(request, "auth/register.html", {"form": form})

        user = form.save()
        login(request, user)

        return redirect("base:home")


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "auth/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)

        if not form.is_valid():
            return render(request, "auth/login.html", {"form": form})

        login(request, form.get_user())

        return redirect("base:home")


class LogoutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        return redirect("base:home")


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, "users/profile.html", {"form": form})


class UpdateProfileView(LoginRequiredMixin, View):
    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)

        if not form.is_valid():
            return render(request, "users/profile.html", {"form": form})

        form.save()

        return redirect("users:profile")