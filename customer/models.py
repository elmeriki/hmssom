from django.db import models
from hmmauth.models import *
from hospital.models import *

# Create your models here.
class Appointment(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    dr = models.ForeignKey(User,on_delete=models.CASCADE)
    visitdsc =  models.TextField(null=True,blank=True)
    date = models.DateField()
    remark =  models.TextField(null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    paymenttype = models.CharField(max_length=200,default=0,null=True,blank=True)
    paymentstatus = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
# Create your models here.
class Prescription(models.Model):
    Hospital = models.ForeignKey(User,on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    dr = models.ForeignKey(User,on_delete=models.CASCADE)
    history =  models.TextField(null=True,blank=True)
    date = models.DateField()
    note =  models.TextField(null=True,blank=True)
    advise =  models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

# Create your models here.
class Medication(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    prescription = models.ForeignKey(Prescription,on_delete=models.CASCADE)
    name =  models.TextField(null=True,blank=True)
    dosage = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)