from django.db import models

# Create your models here.
class Manager(models.Model):
    name = models.CharField(max_length=30)
    uname = models.TextField()
    email = models.CharField(max_length=40,default="@gmail.com")
    ip = models.TextField(default="")
    country = models.TextField(default="")

    

#the follwing part is written only when we use ready made admin
    def __str__(self):
        return self.name 