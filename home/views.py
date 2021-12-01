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


def expenseview(request):

    yearorder = Budget.objects.filter(user=request.user)
    yearlist=[
        {"January":{'Total':0}},{"February":{'Total':0}},{"March":{'Total':0}},{"April":{'Total':0}},{"May":{'Total':0}},{"June ":{'Total':0}},{"July":{'Total':0}},{"August":{'Total':0}},{"September":{'Total':0}},{"October":{'Total':0}},{"November":{'Total':0}},{"December":{'Total':0}}
    ]
    
    for e in yearorder:
        if str(e.date)[0:4]=='2021':
            category=str(e.category).capitalize()
            price=e.cost
            month =list(yearlist[int(str(e.date)[5:7])-1].keys())[0]

            catcost={}
            # #print(month,yearlist[int(str(e.date)[5:7])-1][month].keys())
            if(category in list(yearlist[int(str(e.date)[5:7])-1][month].keys())):
                
                yearlist[int(str(e.date)[5:7])-1][month][category]+=price
                yearlist[int(str(e.date)[5:7])-1][month]['Total']+=price

               
            else:
                yearlist[int(str(e.date)[5:7])-1][month][category]=price
                yearlist[int(str(e.date)[5:7])-1][month]['Total']+=price
              
            # yearlist[int(str(e.date)[5:7])-1][month]


            # category.append(e.category)

            

            #print(catcost)
    #print(yearlist)
        

    return render(request,'Home/expensepage.html',{"yearcost":yearlist,"username":request.user.username})

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

def piechartdata(request,query):

    objects = Budget.objects.filter(user=request.user)

    categories=['food','clothes','groceries','essentials','others']
    categoriescount=[0,0,0,0,0]
    searchmonth = mondict[query[0:3]]
    for ob in objects:
        # print()

        if(int(searchmonth)==int(str(ob.date)[5:7])):
            # print(ob.category)
       
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
    #print(categories,catfinal)
    # print(catfinal,countfinal)


    return {'categories':catfinal,'count':countfinal}



def addpageview(request,slug):
    return render(request,'Home/addpage.html',{"slug":slug})

# Pie Chart
def piechart(request,slug):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    allfigureobjects = PieChart.objects.filter(user=request.user)
    for fig in allfigureobjects:
        if fig.figure:
            fig.figure.delete()
        fig.delete()
    
    piechartdetails=piechartdata(request,slug)
    #print(piechartdetails)

    labels = piechartdetails['categories']
    sizes = piechartdetails['count']
    print(labels,sizes)
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
    figname=str(figureurl)[15:]

  
    return render(request,'Home/piechart.html',{"figureurl":"figures/"+figname,"username":request.user.username})


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
    #print(spends,current_user)
   
    return render(request,"Home/list.html",{"total":cost,"spends":spends,"datelist":slug.split('-'),"username":request.user.username})

def ViewCalendar(request):
    return render(request,'Home/calendar_quarter-year-view.html')

def loginUser(request):
    email=request.POST['email']
    passw = request.POST['password']
    try:
        username = User.objects.get(email=email.lower()).username
    except:
        messages.error(request,"Email Does not exist, Sign up to create an account")
        return redirect("/")


    user = authenticate(username=username, password=passw)
    #print(request.user.is_authenticated)
    
    if user is not None:
        login(request, user)

        return redirect("/")

        # Redirect to a success page.
        ...
    else:
        messages.error(request,"Incorrect Password, Please type the password correctly")
        return redirect("/")
        # Retur

def home(request):
    #print(request.user.is_authenticated)
    if request.user.is_authenticated:
        dates=[]
        dateset= Budget.objects.filter(user=request.user)
        for d in dateset:
            dates.append(str(d.date).split('-'))
        #print(dates)
        context={
           
            "dates":dates,
            "username":request.user.username
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
            messages.error(request,"Email Does not exist, Sign up to create an account")

            return redirect('/signup')
        
    except:
        messages.error(request,"Email Does not exist, Sign up to create an account")
      
    
        return redirect('/signup')

def changepass(request):
    email=request.POST.get('email',False)
    newpass=request.POST['newpass']
    newpassc = request.POST['newpassc']
    #print(email,newpass,newpassc)
    if(newpass==newpassc):
        user= User.objects.get(email=email)
        user.set_password(newpass)
        user.save()
        messages.error(request,"Password Changed, Login with your new password")
        return redirect('/')
    else:
        messages.error(request,"Passwords Don\'t match, please enter again")
        return redirect("/resetpassword")

def forgotPass(request):

    return render(request,'Home/forgotpass.html')


# Create your views here.
