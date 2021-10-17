from django import urls
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path("login",views.login,name="login"),
    path("signup",views.signup,name="signup"),
    path("signupc",views.signupconfirm,name="signupconfirm")

]
