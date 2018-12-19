from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    SignUpView,
    LoginView,
    LogoutView,
    MypageView
)

app_name = 'accounts'

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('mypage', MypageView.as_view(), name='mypage'),
]
