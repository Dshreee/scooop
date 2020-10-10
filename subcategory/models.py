from django.db import models

# Create your models here.
class SubCategory(models.Model):
    name = models.CharField(max_length=30)
    catname = models.CharField(default='0',max_length=100)
    catid = models.IntegerField(default='0')
    

#the follwing part is written only when we use ready made admin
    def __str__(self):
        return self.name + '|' +str(self.pk)