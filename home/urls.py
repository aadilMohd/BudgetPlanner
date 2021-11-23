from django import urls
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path("login",views.loginUser,name="login"),
    path("signup",views.signup,name="signup"),
    path("logout",views.logoutUser,name="signup"),
    path("signupc",views.signupconfirm,name="signupconfirm"),
    path("checkemail",views.CheckemailView,name="checkemail"),
    path("checkemailc", views.Checkemail, name="checkemailconfirm"),
    path("forgotpass",views.forgotPass,name="forgotpass"),
    path("calendar",views.ViewCalendar,name="Calender"),
    path("details/<slug:slug>",views.DetailsView,name="Details"),
    path("resetpassword/",views.changepass,name="changepass"),
    path('pie',views.piechart,name="pie")

]
