from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    SignUpView,
    LoginView,
    LogoutView,
    HistoryView,
)

app_name = 'accounts'

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('history/<int:pk>', HistoryView.as_view(), name='history'),
]
