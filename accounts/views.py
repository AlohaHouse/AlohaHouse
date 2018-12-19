from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    SignUpForm,
    LoginForm,
)
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.contrib.auth import login as django_login


class SignUpView(generic.CreateView):
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:mypage')
    form_class = SignUpForm


class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


class MypageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/mypage.html'
