from django.db import models

# Create your models here.
class Blacklist(models.Model):
    ip = models.CharField(max_length=10)
    
#the follwing part is written only when we use ready made admin
    def __str__(self):
        return self.ip 