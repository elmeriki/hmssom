from django.db import models
from hmmauth.models import *
from hospital.models import *

# Create your models here.
class Appointment(models.Model):
    patient = models.ForeignKey(User,on_delete=models.CASCADE,related_name="patient_appointment_name")
    dr = models.ForeignKey(User,on_delete=models.CASCADE,related_name="dr_who_is_alocated")
    visitdsc =  models.TextField(null=True,blank=True)
    remark =  models.TextField(null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    date = models.DateField(auto_now=True)
    paymenttype = models.CharField(max_length=200,default=0,null=True,blank=True)
    paymentstatus = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Medicine(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hostital_medicine")
    name =  models.CharField(max_length=200,blank=True,null=True,default="None")
    category =  models.CharField(max_length=200,blank=True,null=True,default="None")
    storebox =  models.CharField(max_length=200,blank=True,null=True,default="None")
    purchaseprice=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    saleprice=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    quantity =  models.CharField(max_length=200,blank=True,null=True,default="None")
    genericname =  models.CharField(max_length=200,blank=True,null=True,default="None")
    company =  models.CharField(max_length=200,blank=True,null=True,default="None")
    effects =  models.CharField(max_length=200,blank=True,null=True,default="None")
    expiredate = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Prescription(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_dr_patient_prescription")
    dr = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_dr_gives_prescription")
    patient = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_patient_receives_prescription")
    medicine = models.ForeignKey(Medicine,on_delete=models.CASCADE,blank=True,null=True,related_name="doctor_department")
    history =  models.TextField(null=True,blank=True)
    note =  models.TextField(null=True,blank=True)
    advice =  models.TextField(null=True,blank=True)
    date = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    





    
    
