from django.db import models
from hmmauth.models import *
from hospital.models import *


# Create your models here.
class Appointment(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_appointment_name")
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True,related_name="patient_appointment_name")
    dr=models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True,blank=True,related_name="dr_who_is_alocated")
    visitdsc =  models.TextField(null=True,blank=True)
    remark =  models.TextField(null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    astatus = models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    date =models.DateField(default=0,null=True,blank=True)
    paymenttype = models.CharField(max_length=200,default=0,null=True,blank=True)
    paymentstatus = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Appoint List"
        
    def __str__(self):
        return self.hospital.first_name

class Medicinecategory(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_medicine_for_category")
    categoryname = models.CharField(max_length=200,blank=True,null=True,default="")
    desc = models.CharField(max_length=200,blank=True,null=True,default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    
    class Meta:
        verbose_name_plural = "Medicinecategory"
        
    def __str__(self):
        return self.categoryname
    
class Medicinal(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_medicine")
    category = models.ForeignKey(Medicinecategory,on_delete=models.CASCADE,related_name="hospital_medicine_for_category")
    name =  models.CharField(max_length=200,blank=True,null=True,default="None")
    storebox =  models.CharField(max_length=200,blank=True,null=True,default="None")
    purchaseprice=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    saleprice=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    quantity =  models.CharField(max_length=200,blank=True,null=True,default="None")
    genericname =  models.CharField(max_length=200,blank=True,null=True,default="None")
    company =  models.CharField(max_length=200,blank=True,null=True,default="None")
    effects =  models.CharField(max_length=200,blank=True,null=True,default="None")
    expiredate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Medicinal"
        
    def __str__(self):
        return self.hospital.first_name


class Prescription(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_dr_patient_prescription")
    dr=models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_dr_gives_prescription")
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="hospital_patient_receives_prescription")
    history =  models.CharField(max_length=200,default=0,null=True,blank=True)
    note =  models.CharField(max_length=200,default=0,null=True,blank=True)
    advice =  models.CharField(max_length=200,default=0,null=True,blank=True)
    date = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name_plural = "Prescription"
        
    def __str__(self):
        return self.hospital.first_name



    
    
