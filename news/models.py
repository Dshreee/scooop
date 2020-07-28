from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class News(models.Model):
    name = models.CharField(max_length=30)
    headline = models.CharField(default='-',max_length=100)
    description = models.TextField(default='-')
    #decription = RichTextUploadingField()
    date = models.CharField(max_length=20)
    author = models.CharField(max_length=30)
    picname = models.CharField(max_length=30)
    picurl = models.CharField(default='-',max_length=50)
    categoryname = models.TextField(default='-')
    categoryid = models.IntegerField(default='0')
    ocatid = models.IntegerField(default='0')
    act = models.IntegerField(default=0)#for publish stuff
    show = models.IntegerField(default=0)#for views
    tags = models.TextField(default="")
    

#the follwing part is written only when we use ready made admin
    def __str__(self):
        return self.name + '|' +str(self.pk)