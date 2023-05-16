from django.db import models
from hmmauth.models import *
from hospital.models import *

# Create your models here.
class Appointment(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="patient_appointment_name")
    dr = models.ForeignKey(User,on_delete=models.CASCADE,related_name="dr_who_is_alocated")
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
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_prescription")
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="patient_prescription")
    dr = models.ForeignKey(User,on_delete=models.CASCADE,related_name="dr_who_prescribe")
    history =  models.TextField(null=True,blank=True)
    date = models.DateField()
    note =  models.TextField(null=True,blank=True)
    advise =  models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

# Create your models here.
class Medication(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="patient_medication")
    prescription = models.ForeignKey(Prescription,on_delete=models.CASCADE,related_name="prescription_medication_for_patient")
    name =  models.TextField(null=True,blank=True)
    dosage = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)