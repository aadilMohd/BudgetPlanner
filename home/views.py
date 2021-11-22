from django import http
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Budget
user_here=False
user=None

mondict={
    "Jan":1,
    "Feb":2,
    "Mar":3,
    "Apr":4,
    "May":5,
    "Jun":6,
    "Jul":7,
    "Aug":8,
    "Sep":9,
    "Oct":10,
    "Nov":11,
    "Dec":12
}

def DetailsView(request,slug):

    givendate=slug.split("-")
    monthString=givendate[1]
    day=givendate[2]
    year=givendate[3]
    month=mondict[monthString]

    searchdate = year+'-'+str(month)+'-'+day
    current_user = request.user

    spends = Budget.objects.filter(user=current_user,date=searchdate)
    cost=0
    for x in spends:
        cost+=x.cost
    print(spends,current_user)


    return render(request,"Home/list.html",{"slug":cost})

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

        return redirect("/")

        # Redirect to a success page.
        ...
    else:
        return redirect("/")
        # Retur

   

def home(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        dates=[]
        dateset= Budget.objects.filter(user=request.user)
        for d in dateset:
            dates.append(str(d.date).split('-'))
        print(dates)
        context={
            "message":"hi",
            "dates":dates
        }
        return render(request,'Home/home.html',context)
        
      
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
