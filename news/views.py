from django.shortcuts import render ,get_object_or_404, redirect
from .models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage 
import datetime
from subcategory.models import SubCategory
from category.models import Category
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.

def news_detail(request,pk):
    site = Main.objects.get(pk=2)  
    newsdetail = News.objects.filter(pk=pk)
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Category.objects.all()
    scat = SubCategory.objects.all()
    popnews = News.objects.all().order_by('-show') 
    tagname= News.objects.get(pk=pk).tags
    print(tagname) 
    tag = tagname.split(',')
    try:
        mn = News.objects.get(pk=pk)
        mn.show = mn.show+1
        mn.save()
    except:
        print("cant add show")

    return render(request,'front/news_detail.html',{'news':news,'newsdetail':newsdetail,'site':site,'cat':cat,'scat':scat,'popnews':popnews,'tag':tag})


def news_list(request):
    #authorization check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    # masteruser check
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1

    if perm==0:
        page_obj = News.objects.filter(author=request.user)
    elif perm ==1:
        site = News.objects.all()
        paginator = Paginator(site,4)
        page_no = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_no)

        except EmptyPage:
            page_obj= paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            page_obj= paginator.page(1)

    
    return render(request,'back/news_list.html',{'page_obj':page_obj})

def news_add(request):
    
    #authorization check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    cat = SubCategory.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        headline = request.POST.get('headline')
        author = request.POST.get('author')
        image = request.POST.get('image')
        description = request.POST.get('descrip')
        categoryid = request.POST.get('category')
        view = request.POST.get('view')
        tag = request.POST.get('tag')
       
        now = datetime.datetime.now()
        day = now.day
        month = now.month
        year = now.year 

        if len(str(day)) == 1 :
            day = "0"+str(day)

        if len(str(month)) == 1 :
            month = "0"+str(month)

        today = str(year) + "/" + str(month) + "/" + str(day)

        if headline == "" or description == "":
                
            error='Mandatory fields are required ..'
            return render(request,'back/error.html',{'error':error})

        #try:
        file = request.FILES["image"]
        fs = FileSystemStorage()
        filename = fs.save(file.name ,file)
        url = fs.url(filename)

        if str(file.content_type).startswith("image"):
                    
            if file.size<5000000:
                        
                categoryname = SubCategory.objects.get(pk=categoryid).name   
                ocatid = SubCategory.objects.get(pk=categoryid).catid    
                b = News(name=name,headline=headline,description=description,date=today,author=request.user,picname=filename,picurl=url,categoryname=categoryname,categoryid=categoryid,ocatid=ocatid,tags=tag)    
                b.save()                    
                        
                count = len(News.objects.filter(ocatid=ocatid))
                c = Category.objects.get(pk=ocatid)
                c.count = count 
                c.save()


                return redirect('news_list')
            else :
                error='Please select an image size less than 5MB!!'
                return render(request,'back/error.html',{'error':error})
            
        else:
            fs = FileSystemStorage()
            fs.delete(filename)
            error='Please select an image type file!!'
            return render(request,'back/error.html',{'error':error})

        #except :
            #error='Please select image file to be uploaded !!'
            #return render(request,'back/error.html',{'error':error})

    return render(request,'back/news_add.html',{'cat':cat})

def news_delete(request,pk):
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

    b=News.objects.get(pk=pk)
    fs = FileSystemStorage()
    fs.delete(b.picname)

    ocatid = News.objects.get(pk=pk).ocatid

    b.delete()
    count = len(News.objects.filter(ocatid=ocatid))
    c = Category.objects.get(pk=ocatid)
    c.count = count 
    c.save()
    return redirect('news_list')

def news_edit(request,pk):
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

    if len(News.objects.filter(pk=pk))==0:
        error='News not found !!'
        return render(request,'back/error.html',{'error':error})
    
    news = News.objects.get(pk=pk)
    cat = SubCategory.objects.all()

   
    if request.method == 'POST':
        name = request.POST.get('name')
        headline = request.POST.get('headline')
        image = request.POST.get('image')
        description = request.POST.get('description')
        categoryid = request.POST.get('category')
        view = request.POST.get('view')
        tag = request.POST.get('tag')
       
       
        now = datetime.datetime.now()
        day = now.day
        month = now.month
        year = now.year 

        if len(str(day)) == 1 :
            day = "0"+str(day)

        if len(str(month)) == 1 :
            month = "0"+str(month)

        today = str(year) + "/" + str(month) + "/" + str(day)
        
        if headline == "" or description == "":
                
            error='Mandatory fields are required ..'
            return render(request,'back/error.html',{'error':error})

        try:
            file = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(file.name ,file)
            url = fs.url(filename)
            
            if str(file.content_type).startswith("image"):
                
                if file.size<5000000:
                    categoryname = SubCategory.objects.get(pk=categoryid).name
                    b = News.objects.get(pk=pk)
                    fss = FileSystemStorage()
                    fss.delete(b.picname)
                    

                    b = News.objects.get(pk=pk)
                    b.name = name
                    b.headline = headline
                    b.description = description
                    b.view = view
                    b.picname = filename
                    b.picurl = url
                    b.categoryname=categoryname
                    b.categoryid = categoryid
                    b.act = 0
                    b.tags=tag
                    b.save()

                    return redirect('news_list')
                else :
                    error='Please select an image size less than 5MB!!'
                    return render(request,'back/error.html',{'error':error})
           
            else:
                fs = FileSystemStorage()
                fs.delete(filename)
                error='Please select an image type file!!'
                return render(request,'back/error.html',{'error':error})

        except :
            
            categoryname = SubCategory.objects.get(pk=categoryid).name
            b = News.objects.get(pk=pk)
            b.name = name
            b.headline = headline
            b.description = description
            b.view = view
            b.categoryname=categoryname
            b.categoryid = categoryid
            b.act = 0 
            b.tags=tag       
            b.save()

            return redirect('news_list')          
    

    return render(request,'back/news_edit.html',{'pk':pk,'news':news,'cat':cat})

def news_publish(request,pk):
    #authorization check
    if not request.user.is_authenticated:
        return redirect('mylogin')
    
    news = News.objects.get(pk=pk)
    news.act = 1
    news.save()
    return redirect('news_list')

def news_all_show(request,word):
    catid = Category.objects.get(name=word).pk
    allnews = News.objects.filter(ocatid=catid)

    site=Main.objects.get(pk=2)  #Main object(2) in admin
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Category.objects.all()
    scat = SubCategory.objects.all()
    latestnews = News.objects.filter(act=1).order_by('-pk')[:3] #act is used for knowing if the news is published or not
    latestnews2 = News.objects.filter(act=1).order_by('-pk')[:4]
    popnews = News.objects.all().order_by('-show')
    return render(request,'front/all_news.html',{'site':site,'news':news,'cat':cat,'scat':scat,'latestnews':latestnews,'latestnews2':latestnews2,'allnews':allnews,'word':word,'popnews':popnews})


   