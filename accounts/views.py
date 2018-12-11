from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm


class SignUpView(generic.CreateView):
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:signup')
    form_class = SignUpForm
