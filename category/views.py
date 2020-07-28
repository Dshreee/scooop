from django.shortcuts import render ,get_object_or_404, redirect
from .models import Category
import csv #for csv file
from django.http import HttpResponse  #for csv file

# Create your views here.

def category_list(request):
    cat = Category.objects.all()  
    
    return render(request,'back/category_list.html',{'cat':cat})


def category_add(request):
    cat = Category.objects.all()  
    
    if request.method =='POST':

        name = request.POST.get('name')

        if name=='':
            error='Mandatory fields are required ..'
            return render(request,'back/error.html',{'error':error})
        
        if len(Category.objects.filter(name=name))!=0 :
            error='Category is already available ..'
            return render(request,'back/error.html',{'error':error})

        b = Category(name=name)
        b.save()
        return redirect('category_list')

    return render(request,'back/category_add.html')

def export_cat_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename="category.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name','Counter'])
    for i in Category.objects.all():
        writer.writerow([i.name,i.count])

    return response

def import_cat_csv(request):

    if request.method=="POST":
        csv_file=request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            error='Please input CSV file'
            return render(request,'back/error.html',{'error':error})

        if csv_file.multiple_chunks():
            error='File too large'
            return render(request,'back/error.html',{'error':error})

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        for line in lines:
            fields = line.split(",")
            try:
                if len(Category.objects.filter(name=fields[0]))==0 and fields[0]!="Name" and fields[0]!="":
                    b = Category(name=fields[0])
                    b.save()
            
            except:
                print("finish")

    return redirect('category_list')