from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)
from django.contrib.auth import get_user_model

import re

# プロジェクトで使用しているUserモデルを取得
User = get_user_model()


class SignUpForm(UserCreationForm):
    """ユーザーの登録"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username","email","password1", "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields.get('username').widget.attrs['placeholder'] ='Username'
        self.fields.get('email').widget.attrs['placeholder'] ='Email'
        self.fields.get('password1').widget.attrs['placeholder'] ='Password'
        self.fields.get('password2').widget.attrs['placeholder'] ='Confirm Password'

    
    def clean_email(self):
        email = self.cleaned_data['email']

        result = re.match('^[a-z0-9]+\.[a-z0-9]+@m.alhinc.jp$',email)
        if not result:
            raise forms.ValidationError("メールちがう")
        return email


class LoginForm(AuthenticationForm):
    """ログイン"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields.get('username').widget.attrs['placeholder'] ='Username'
        self.fields.get('password').widget.attrs['placeholder'] ='Password'
        
        
