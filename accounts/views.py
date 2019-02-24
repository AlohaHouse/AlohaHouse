from django.shortcuts import render, redirect, get_object_or_404
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
from article.models import (
    History,
    Favorite
)


class SignUpView(generic.CreateView):
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:mypage')
    form_class = SignUpForm


class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

class HistoryView(LoginRequiredMixin, generic.TemplateView):
    sucssece_url = 'article:result'

    def get(self, request, **kwargs):
        pk = kwargs['pk']
        history = get_object_or_404(History, pk=pk)
        url = history.url
        request.session['history_url'] = url
        return redirect(self.sucssece_url)