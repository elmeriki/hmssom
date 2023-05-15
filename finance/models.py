from django.db import models
from hmmauth.models import *
from hospital.models import *


# Create your models here.
class Paymentcategory(models.Model):
    Hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name='hospital_name')
    category = models.CharField(max_length=200,default=0,null=True,blank=True)
    dec =  models.TextField(null=True,blank=True)
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
# Create your models here.
class Appointment(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    visitdsc =  models.TextField(null=True,blank=True)
    dob = models.DateField()
    pname =  models.TextField(null=True,blank=True)
    paymentcategory = models.ForeignKey(Paymentcategory,on_delete=models.CASCADE)
    pnumber = models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    paymenttype = models.CharField(max_length=200,default=0,null=True,blank=True)
    paymentstatus = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    

# Create your models here.
class Expense(models.Model):
    Hospital = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
