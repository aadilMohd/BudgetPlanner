from django.http.response import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request,'Home/login.html')


def login(request):
    username=request.POST['uname']
    passw = request.POST['pass']
    print(username,passw)
    
    return HttpResponse("Login page")

# Create your views here.
