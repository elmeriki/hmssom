from django.db import models
from hmmauth.models import *
from hospital.models import *


# Create your models here.

class Paymentcategory(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name='hospital_category_name')
    category = models.CharField(max_length=200,default=0,null=True,blank=True)
    dec=models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Payment(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name='payment_category_for_hospital')
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="payment_for_patient")
    category = models.ForeignKey(Paymentcategory,on_delete=models.CASCADE,related_name="payment_category")
    treatedby_dr = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name="doctor_who_treated_patient")
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    visitdsc =  models.TextField(null=True,blank=True)
    paymenttype = models.CharField(max_length=200,default=0,null=True,blank=True)
    paymentstatus = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Expensescategory(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="expenses_for_category")
    name = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Expense(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="expenses_for_hospital")
    category = models.ForeignKey(Expensescategory,on_delete=models.CASCADE,related_name="expenses_for_categories")
    decs = models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
