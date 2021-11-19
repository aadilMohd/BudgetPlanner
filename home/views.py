from django import http
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
user_here=False
user=None


def DetailsView(self,slug):

    return HttpResponse("hi"+slug)

def ViewCalendar(request):
    return render(request,'Home/calendar_quarter-year-view.html')
def loginUser(request):
    email=request.POST['email']
    passw = request.POST['password']
    username = User.objects.get(email=email.lower()).username
    user = authenticate(username=username, password=passw)
    print(request.user.is_authenticated)
    
    if user is not None:
        login(request, user)

        return render(request,'Home/home.html')

        # Redirect to a success page.
        ...
    else:
        return render(request,'Home/login.html')
        # Retur

   

def home(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return render(request,'Home/home.html',{"ex":[[2021,6,6],[2021,6,7],[2021,5,3]]})
        
      
    return render(request,'Home/login.html')


    # if request.user.is_authenticated():
    #     return HttpResponse("User alrrady Logged in")
    

def signup(request):

    return render(request,'Home/signup.html')

def logoutUser(request):
    logout(request)
    return redirect('/')



def signupconfirm(request):

    fullname= request.POST['username']
    phone= request.POST['phone']
    email= request.POST['email']
    pass1= request.POST['password']
    pass2 = request.POST['confpassword']

    user = User.objects.create_user(fullname,email,pass1)
    user.phone=phone
    user.save()

    login(request,user)


    return redirect('/')
def CheckemailView(request):
    return render(request,'Home/forgotpass.html')
def Checkemail(request):
    email = request.POST['email']

    try:

        if User.objects.get(email=email):
            return HttpResponse("email confirmed")
        else:
            return redirect('/signup')
        
    except:
    
        return redirect('/signup')

def forgotPass(request):

    return render(request,'Home/forgotpass.html')


# Create your views here.
