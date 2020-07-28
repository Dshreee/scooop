from django.shortcuts import render ,get_object_or_404, redirect
from .models import SubCategory
from category.models import Category

# Create your views here.

def subcategory_list(request):
    #authorization check
    if not request.user.is_authenticated:
        return redirect('mylogin')
        
    scat = SubCategory.objects.all()  
    
    return render(request,'back/subcategory_list.html',{'scat':scat})


def subcategory_add(request):
    #authorization check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    cat = Category.objects.all()  
    
    if request.method =='POST':

        name = request.POST.get('name')
        catid = request.POST.get('category')
        catname = Category.objects.get(pk=catid).name

        if name=='':
            error='Mandatory fields are required ..'
            return render(request,'back/error.html',{'error':error})
        
        if len(SubCategory.objects.filter(name=name))!=0 :
            error='Category is already available ..'
            return render(request,'back/error.html',{'error':error})

        b = SubCategory(name=name,catname=catname,catid=catid)
        b.save()
        return redirect('subcategory_list')

    return render(request,'back/subcategory_add.html',{'cat':cat})


