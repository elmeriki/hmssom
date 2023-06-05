from django.db import models
from django.contrib.auth.models import AbstractUser
from hmmauth.models import *


class User(AbstractUser):
    is_hospital = models.BooleanField(default=False,blank=True,null=True)
    is_dr = models.BooleanField(default=False,blank=True,null=True)
    is_customer = models.BooleanField(default=False,blank=True,null=True)
    is_activation = models.BooleanField(default=False,blank=True,null=True)
    customerid =  models.CharField(max_length=200,blank=True,null=True,default="None")
    address =  models.CharField(max_length=200,blank=True,null=True,default="None")
    country =  models.CharField(max_length=200,blank=True,null=True,default="None")
    city =  models.CharField(max_length=200,blank=True,null=True,default="None")
    number =  models.CharField(max_length=200,blank=True,null=True,default="None")
    def __str__(self):
        return self.username
    
    class Meta(AbstractUser.Meta):
       swappable = 'AUTH_USER_MODEL'
       
class Passcode(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_names_passcode")
    password =  models.CharField(max_length=200,blank=True,null=True,default="None")
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)