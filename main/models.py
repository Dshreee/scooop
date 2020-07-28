from django.db import models

# Create your models here.
class Main(models.Model):
    name = models.CharField(max_length=30)
    about = models.TextField()
    aboutus = models.TextField(default="")
    tel = models.CharField(default='987654321',max_length=30)
    fblink = models.CharField(default='#',max_length=30)
    twlink = models.CharField(default='#',max_length=30)
    ytlink = models.CharField(default='#',max_length=30)
    set_name = models.CharField(default='-',max_length=30)


#the follwing part is written only when we use ready made admin
    def __str__(self):
        return self.set_name +" | "+ str(self.pk) #this is used to know the pika no.