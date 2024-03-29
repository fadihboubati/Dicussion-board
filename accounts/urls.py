"""dicussion_board URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/pages/login.html'), name='login'),
    path('settings/change_password/', auth_views.PasswordChangeView.as_view(template_name='accounts/pages/change_password.html'), name='password_change'),
    path('settings/change_password_done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/pages/change_password_done.html'), name='password_change_done'),
    path('account/', views.UserUpdateView.as_view(), name='my_account'),
]
