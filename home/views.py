from django import http
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Budget, PieChart
import matplotlib
from matplotlib import pyplot as plt
import random
from django.core.files.base import ContentFile
from django.contrib import messages
import io
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

def addtodb(request,slug):

    givendate=slug.split("-")
    monthString=givendate[1]
    day=givendate[2]
    year=givendate[3]
    month=mondict[monthString]

    searchdate = year+'-'+str(month)+'-'+day


    desc=request.GET['description']
    category=request.GET['category']
    cost=request.GET['amount']

    ob = Budget(id=random.randint(1,7555555),user=request.user,date=searchdate,category=category,description=desc,cost=cost)
    ob.save()



    return redirect('/details/'+slug)

def piechartdata(request):

    objects = Budget.objects.filter(user=request.user)

    categories=['food','clothes','groceries','essentials','others']
    categoriescount=[0,0,0,0,0]
    for ob in objects:
       
        if ob.category.lower() == 'food':
            categoriescount[0]+=ob.cost
        elif ob.category.lower() == 'clothes':
            categoriescount[1]+=ob.cost
        elif ob.category.lower() == 'groceries':
            categoriescount[2]+=ob.cost
        elif ob.category.lower() == 'essesntials':
            categoriescount[3]+=ob.cost
        else:
            categoriescount[4]+=ob.cost
      
    catfinal = [categories[x] for x in range(len(categories)) if categoriescount[x]!=0]
    countfinal = [x for x in categoriescount if x !=0]
    print(categories,catfinal)
    print(categoriescount,countfinal)


    return {'categories':catfinal,'count':countfinal}



def addpageview(request,slug):
    return render(request,'Home/addpage.html',{"slug":slug})

# Pie Chart
def piechart(request):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    allfigureobjects = PieChart.objects.filter(user=request.user)
    for fig in allfigureobjects:
        if fig.figure:
            fig.figure.delete()
        fig.delete()
    
    piechartdetails=piechartdata(request)
    print(piechartdetails)

    labels = piechartdetails['categories']
    sizes = piechartdetails['count']
    explode = (0.1, 0,0,0,0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    # fig1, ax1 = plt.subplots()
    fig1 = plt.figure()
    ax1 = fig1.add_axes([0,0,1,1])
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
      # Equal aspect ratio ensures that pie is drawn as a circle.
    f=io.BytesIO()
    plt.savefig(f)
    content_file = ContentFile(f.getvalue())
    model_object = PieChart.objects.create(user=request.user)
   
    model_object.figure.save('chart1', content_file)
    model_object.save()

    figureurl =PieChart.objects.filter(user=request.user).first().figure
  
    return render(request,'Home/piechart.html',{"figureurl":figureurl})


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
   


    return render(request,"Home/list.html",{"total":cost,"spends":spends,"datelist":slug.split('-')})

def ViewCalendar(request):
    return render(request,'Home/calendar_quarter-year-view.html')

def loginUser(request):
    email=request.POST['email']
    passw = request.POST['password']
    try:
        username = User.objects.get(email=email.lower()).username
    except:
        messages.error(request,"Email Doesn't exist, Sign up to create an account")
        return redirect("/")


    user = authenticate(username=username, password=passw)
    print(request.user.is_authenticated)
    
    if user is not None:
        login(request, user)

        return redirect("/")

        # Redirect to a success page.
        ...
    else:
        messages.error(request,"Incorrect Password, Please type the password corectly")
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
            messages.error(request,"Email Confirmed, You can change your password")
            return render(request,'Home/changepass.html')
        else:
            messages.error(request,"Email Doesn't exist, Sign up to create an account")

            return redirect('/signup')
        
    except:
        messages.error(request,"Email Doesn't exist, Sign up to create an account")
      
    
        return redirect('/signup')

def changepass(request):
    email=request.POST['email']
    newpass=request.POST['newpass']
    newpassc = request.POST['newpassc']
    print(email,newpass,newpassc)
    if(newpass==newpassc):
        user= User.objects.get(email=email)
        user.set_password(newpass)
        user.save()
        messages.error(request,"Password Changed, Login with your new password")
        return redirect('/')
    else:
        messages.error(request,"Passwords Don't match, please enter again")
        return redirect("/resetpassword")

def forgotPass(request):

    return render(request,'Home/forgotpass.html')


# Create your views here.
