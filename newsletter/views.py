from django.shortcuts import render ,get_object_or_404, redirect
from .models import Newsletter
from news.models import News
from category.models import Category
from subcategory.models import SubCategory
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,Group,Permission
from django.contrib.contenttypes.models import ContentType
import csv #for csv file
from django.http import HttpResponse  #for csv file


# Create your views here.
def newsletter(request):
    if request.method =="POST":
        txt = request.POST.get('contact')
        e = txt.find('@')
        if int(e) != -1:
            n = Newsletter(txt=txt,status=1)
            n.save()
        else:
            try:
                int(txt)
                n = Newsletter(txt=txt,status=2)
                n.save()
            except:
                return redirect('home')

    return redirect('home')

def newsletter_email(request):
    #authorization check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    em = Newsletter.objects.filter(status=1) 

    return render(request,'back/email.html',{'em':em})

def newsletter_contact(request):
    #authorization check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    cn = Newsletter.objects.filter(status=2)

    return render(request,'back/contactno.html',{'cn':cn})

def newsletter_del(request,pk,status):
    #authorization check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    b = Newsletter.objects.get(pk=pk)
    b.delete()

    if int(status)==2:
        return redirect('newsletter_contact')
    else:
        return redirect('newsletter_email')

    return render(request,'back/contactno.html',{'cn':cn})

def export_newsletter_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename="newsletter_email.csv"'
    writer = csv.writer(response)
    writer.writerow(['Email'])
    for i in Newsletter.objects.filter(status=1):
        writer.writerow([i.txt])

    return response