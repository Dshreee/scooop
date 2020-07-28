from django.shortcuts import render ,get_object_or_404, redirect
from .models import Manager
from news.models import News
from category.models import Category
from subcategory.models import SubCategory
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,Group,Permission
from django.contrib.contenttypes.models import ContentType

# Create your views here.

def manager_list(request):

    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end

    man = Manager.objects.all().exclude(uname="admin")
    return render(request,'back/manager_list.html',{'man':man})

def manager_delete(request,pk):
    
    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end
    
    manager = Manager.objects.get(pk=pk)
    b = User.objects.get(username=manager.uname)
    b.delete()
    manager.delete()

    return redirect('manager_list')

def manager_group(request):
    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end

    grp = Group.objects.all().exclude(name = "masteruser")
    return render(request,'back/manager_group.html',{'grp':grp})

def manager_group_add(request):
    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end

    if request.method == "POST":
        name = request.POST.get('name')
    
    if name!="":
        if len(Group.objects.filter(name=name))==0:
            group = Group(name=name)
            group.save()

    return redirect('manager_group')

def manager_group_delete(request,name):
    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end


    b = Group.objects.filter(name=name)
    b.delete()

    return redirect('manager_group')

def user_groups(request,pk):
    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end
    

    mng = Manager.objects.get(pk=pk)
    user = User.objects.get(username=mng)
    ugroup = []
    for i in user.groups.all():
        ugroup.append(i.name)

    group = Group.objects.all()
    return render(request,'back/user_groups.html',{'ugroup':ugroup,'group':group,'pk':pk})

def add_user_to_group(request,pk):
    
    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end
    
    if request.method == "POST":

        gname = request.POST.get('gname')
        grp = Group.objects.get(name=gname)
        manager = Manager.objects.get(pk=pk)
        usr = User.objects.get(username=manager.uname)
        usr.groups.add(grp)

    return redirect('user_groups',pk=pk)

def del_user_from_group(request,pk,name):
    
    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end
    
    grp = Group.objects.get(name=name)
    manager = Manager.objects.get(pk=pk)
    usr = User.objects.get(username=manager.uname)
    usr.groups.remove(grp)

    return redirect('user_groups',pk=pk)

def manager_perm(request):
    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end

    perm = Permission.objects.all()
    return render(request,'back/manager_perm.html',{'perm':perm})

def manager_perm_del(request,name):
    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end

    perm = Permission.objects.filter(name=name)
    perm.delete()
    return redirect('manager_perm')

def manager_perm_add(request):
    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end

    if request.method =="POST" :
        name = request.POST.get('name')
        cname = request.POST.get('cname')

        if len(Permission.objects.filter(codename=cname))==0:
            content_type = ContentType.objects.get(app_label='main',model='main')
            p = Permission.objects.create(codename=cname,name=name,content_type=content_type)
        
        else:
            error='The codename is already available'
            return render(request,'back/error.html',{'error':error})

    return redirect('manager_perm')

def user_perms(request,pk):
    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end
    

    mng = Manager.objects.get(pk=pk)
    user = User.objects.get(username=mng)
    permission = Permission.objects.filter(user=user)

    uperms = []
    for i in permission:
        uperms.append(i.name)

    perms = Permission.objects.all()

    return render(request,'back/user_perms.html',{'uperms':uperms,'pk':pk,'perms':perms})

def user_perms_del(request,pk,name):
    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end
    mng = Manager.objects.get(pk=pk)
    user = User.objects.get(username=mng.uname)
    permission = Permission.objects.get(name=name)
    user.user_permissions.remove(permission)

    return redirect('user_perms',pk=pk)

def user_perms_add(request,pk):
    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end

    if request.method =='POST':
        pname = request.POST.get('pname')
        mng = Manager.objects.get(pk=pk)
        user = User.objects.get(username=mng.uname)
        permission = Permission.objects.get(name=pname)
        user.user_permissions.add(permission)
   

    return redirect('user_perms',pk=pk)

def group_perms(request,name):
    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end
    
    group = Group.objects.get(name=name)
    gperms= group.permissions.all()
    allperms = Permission.objects.all()

    return render(request,'back/group_perms.html',{'gperms':gperms,'name':name,'allperms':allperms})

def group_perms_del(request,gname,name):
    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end
    group = Group.objects.get(name=gname)
    perm = Permission.objects.get(name=name)
    group.permissions.remove(perm)

    return redirect('group_perms',name=gname)

def group_perms_add(request,name):
    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        error='Access Denied'
        return render(request,'back/error.html',{'error':error})
    # masteruser check end

    if request.method=="POST":
        pname = request.POST.get('pname')
        group = Group.objects.get(name=name)
        perm = Permission.objects.get(name=pname)
        group.permissions.add(perm)

    return redirect('group_perms',name=name)