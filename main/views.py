from django.shortcuts import render ,get_object_or_404, redirect
from .models import Main
from news.models import News
from category.models import Category
from subcategory.models import SubCategory
from manager.models import Manager
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,Group,Permission
from ipware import get_client_ip #to get the ip address
from ip2geotools.databases.noncommercial import DbIpCity #to get the city via ip address

# Create your views here.
def home(request):
    site=Main.objects.get(pk=1)  #Main object(1) in admin
    news = News.objects.filter(act=1).order_by('-pk')
    news2 = News.objects.filter(act=1).order_by('-pk')[:6]
    cat = Category.objects.all()
    scat = SubCategory.objects.all()
    latestnews = News.objects.filter(act=1).order_by('-pk')[:3] #act is used for knowing if the news is published or not
    latestnews2 = News.objects.filter(act=1).order_by('-pk')[4:8]
    popnews = News.objects.filter(act=1).order_by('-show')
    return render(request,'front/home.html',{'site':site,'news':news,'cat':cat,'scat':scat,'latestnews':latestnews,'latestnews2':latestnews2,'popnews':popnews,'news2':news2})


def about(request):
    sitename = 'ABOUT'
    site=Main.objects.get(pk=1)  #Main object(2) in admin
    news = News.objects.filter(act=1).order_by('-pk')
    news2 = News.objects.filter(act=1).order_by('-pk')[:6]
    cat = Category.objects.all()
    scat = SubCategory.objects.all()
    latestnews = News.objects.filter(act=1).order_by('-pk')[:3] #act is used for knowing if the news is published or not
    latestnews2 = News.objects.filter(act=1).order_by('-pk')[4:8]
    popnews = News.objects.filter(act=1).order_by('-show')
    return render(request,'front/about.html',{'sitename':sitename,'site':site,'news':news,'cat':cat,'scat':scat,'latestnews':latestnews,'latestnews2':latestnews2,'popnews':popnews,'news2':news2})  

def panel(request):
    
    #authorization check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    perm =0
    for i in request.user.groups.all():
        if i.name=="masteruser" or i.name=="content writers" :perm = 1
    
    if perm == 1:
        return render(request,'back/home.html')
    else:
        return redirect('home')

def mylogin(request):
    if request.method=='POST':
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        
        if user!="" and pwd!="" :
            u = authenticate(username=user ,password=pwd)
            if u!= None:
                login(request,u)
                return redirect('panel')

    return render(request,'front/login.html')
    
def mylogout(request):
    logout(request)
    return redirect('mylogin')

def changepass(request):
    #authorization check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    if request.method=='POST':
        oldpwd = request.POST.get('oldpass')
        newpwd = request.POST.get('newpass')

        if oldpwd =='' and newpwd =='':
            error='All fields are required ..'
            return render(request,'back/error.html',{'error':error})

        user = authenticate(username=request.user ,password=oldpwd)

        if user!= None:
            
            if len(newpwd)<8:
                error='Password must be atleast 8 characters long'
                return render(request,'back/error.html',{'error':error})

            c1=0
            c2=0
            c3=0
            c4=0
            for i in newpwd:
                if i > "0" and i < "9":
                    c1=1
                if i > "A" and i < "Z":
                    c2=1
                if i > "a" and i < "z":
                    c3=1
                if i > "!" and i < "(":
                    c4=1
                
            if c1==1 and c2==1 and c3==1 and c4==1:
                user = User.objects.get(username=request.user)
                user.set_password(newpwd)
                user.save()
                return redirect('mylogout')
                
        else:
            error='Incorrect Password !!'
            return render(request,'back/error.html',{'error':error})

    return render(request,'back/changepass.html')

def myregister(request):
    if request.method=='POST':
        name = request.POST.get('name')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pwd1 = request.POST.get('password1')
        pwd2 = request.POST.get('password2')

        if pwd1!=pwd2:
            msg = "Your passwords did'nt match "
            return render(request,'front/msgbox.html',{'msg':msg})

        if len(pwd1)<8:
                msg='Password must be atleast 8 characters long'
                return render(request,'front/msgbox.html',{'msg':msg})

        c1=0
        c2=0
        c3=0
        c4=0
        for i in pwd1:
            if i > "0" and i < "9":
                c1=1
            if i > "A" and i < "Z":
                c2=1
            if i > "a" and i < "z":
                c3=1
            if i > "!" and i < "(":
                c4=1
                
            if c1==0 and c2==0 and c3==0 and c4==0:
                msg='Password is not strong'
                return render(request,'front/msgbox.html',{'msg':msg})

    ip,is_routable= get_client_ip(request)
    if ip is None:
        ip="0.0.0.0"

    try:
        response = DbIpCity.get(ip,aip_keys='free') #we will get the country name only when the ip address is public
        country =response.country+'|'+response.city 

    except:
        country="unknown"

    #check if the entered username and email is already available or not
    if len(User.objects.filter(username=uname))==0 and len(User.objects.filter(email=email))==0:
        u = User.objects.create_user(username=uname,email=email,password=pwd1)
        b = Manager(name=name,uname=uname,email=email,ip=ip,country=country) 
        b.save()    

    return render(request,'front/login.html')

def site_settings(request):
     #authorization check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    # masteruser check and also if some other user tries to delete the news 
    # via url then this section will not let that happen
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        a = News.objects.get(pk=pk).author
        if str(a)!=str(request.user):
            error='Access Denied'
            return render(request,'back/error.html',{'error':error})
    # masteruser check end

    if request.method=='POST':
        sitename = request.POST.get('sitename')
        tel = request.POST.get('tel')
        fblink = request.POST.get('fblink')
        twlink = request.POST.get('twlink')
        ytlink = request.POST.get('ytlink')
        about = request.POST.get('about')
        aboutus = request.POST.get('aboutus')

        if fblink == "" : fblink = "#"
        if twlink == "" : twlink = "#"
        if ytlink == "" : ytlink = "#"
        
        if sitename == "" or tel == "" or about == "" :
            error = "All Fields Requirded"
            return render(request, 'back/error.html' , {'error':error})

        b = Main.objects.get(pk=1)
        b.name = sitename
        b.tel = tel
        b.fblink = fblink
        b.twlink = twlink
        b.ytlink = ytlink
        b.about = about
        b.aboutus = aboutus
        
        b.save()
    site = Main.objects.get(pk=1)    
    return render(request,'back/setting.html',{'site':site})