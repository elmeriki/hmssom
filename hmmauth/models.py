from django.db import models
from django.contrib.auth.models import AbstractUser
from hmmauth.models import *



class User(AbstractUser):
    is_admin = models.BooleanField(default=False,blank=True,null=True)
    is_dr = models.BooleanField(default=False,blank=True,null=True)
    is_customer = models.BooleanField(default=False,blank=True,null=True)
    is_activation = models.BooleanField(default=False,blank=True,null=True)
    customerid =  models.CharField(max_length=200,blank=True,null=True,default="None")
    address =  models.CharField(max_length=200,blank=True,null=True,default="None")
    country =  models.CharField(max_length=200,blank=True,null=True,default="None")
    city =  models.CharField(max_length=200,blank=True,null=True,default="None")
    number =  models.CharField(max_length=200,blank=True,null=True,default="None")
    def __str__(self):
        return self.hname
    
    class Meta(AbstractUser.Meta):
       swappable = 'AUTH_USER_MODEL'