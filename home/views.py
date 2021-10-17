from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

user_here=False

def home(request):
    if user_here:
        return HttpResponse("Hi")
    return render(request,'Home/login.html')


def login(request):
    usern=request.POST['uname']
    passw = request.POST['pass']
    user = authenticate(username=usern, password=passw)
    if user is not None:
        user_here=True
        print(usern)
        return HttpResponse("Logged in")

    return HttpResponse("Not Logged in page")

def signup(request):

    return render(request,'Home/signup.html')

def signupconfirm(request):

    fullname= request.POST['fname']
    phone= request.POST['number']
    email= request.POST['uemail']
    pass1= request.POST['pass']
    pass2 = request.POST['passc']

    user = User.objects.create_user(fullname,email,pass1)
    user.phone=phone
    user.save()



    


    return HttpResponse("Signup Confirmed"+fullname)

# Create your views here.
