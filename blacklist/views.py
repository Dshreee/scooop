from django.shortcuts import render ,get_object_or_404, redirect
from .models import Blacklist
from news.models import News
from category.models import Category
from subcategory.models import SubCategory
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,Group,Permission
from django.contrib.contenttypes.models import ContentType

# Create your views here.
def blacklist(request):
    blist = Blacklist.objects.all()
    return render(request,'back/blacklist.html',{'blist':blist})

def blacklist_add(request):
     # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end

    if request.method == "POST":
        ipadd = request.POST.get('ipadd')
    
    if ipadd!="":
        if len(Blacklist.objects.filter(ip=ipadd))==0:
            bl = Blacklist(ip=ipadd)
            bl.save()

    return redirect('blacklist')

def blacklist_delete(request,ip):
    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end


    b = Blacklist.objects.filter(ip=ip)
    b.delete()

    return redirect('blacklist')