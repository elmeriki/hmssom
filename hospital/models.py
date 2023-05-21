from django.db import models
from hmmauth.models import *

# Create your models here.
class Hospital(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_names")
    hospitalid =  models.CharField(max_length=200,blank=True,null=True,default="None")
    package =  models.CharField(max_length=200,blank=True,null=True,default="None")
    desc=models.TextField(null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Department(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_diff_departments")
    name =  models.CharField(max_length=200,blank=True,null=True,default="None")
    desc=  models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
# Create your models here.
class Doctor(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="doctor_belogs_to_hospital_names")
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="hospital_doctor_name")
    department = models.ForeignKey(Department,on_delete=models.CASCADE,blank=True,null=True,related_name="doctor_department")
    name =  models.CharField(max_length=200,blank=True,null=True,default="None")
    phone =  models.CharField(max_length=200,blank=True,null=True,default="None")
    email =  models.CharField(max_length=200,blank=True,null=True,default="None")
    address =  models.CharField(max_length=200,blank=True,null=True,default="None")
    signature = models.ImageField(null=True, upload_to="doctors_signature/",)
    picture = models.ImageField(null=True, upload_to="doctors_pictures/",)
    profile=  models.TextField(null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    

# Create your models here.
class Humanresource(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_human_resource")
    category = models.CharField(max_length=200,blank=True,null=True,default="None")
    employeeid =  models.CharField(max_length=200,blank=True,null=True,default="None")
    title =  models.CharField(max_length=200,blank=True,null=True,default="None")
    name =  models.CharField(max_length=200,blank=True,null=True,default="None")
    email =  models.CharField(max_length=200,blank=True,null=True,default="None")
    address =  models.CharField(max_length=200,blank=True,null=True,default="None")
    phone =  models.CharField(max_length=200,blank=True,null=True,default="None")
    signature = models.ImageField(null=True, upload_to="employee_signature/",)
    picture = models.ImageField(null=True, upload_to="employee_pictures/",)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Patient(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_patient_is_admitted")
    patientid =  models.CharField(max_length=200,blank=True,null=True,default="None")
    title =  models.CharField(max_length=200,blank=True,null=True,default="None")
    name =  models.CharField(max_length=200,blank=True,null=True,default="None")
    nok =  models.CharField(max_length=200,blank=True,null=True,default="None")
    non =  models.CharField(max_length=200,blank=True,null=True,default="None")
    phone =  models.CharField(max_length=200,blank=True,null=True,default="None")
    paymenttype =  models.CharField(max_length=200,blank=True,null=True,default="None")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Labtest(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hostital_lab_test")
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="patient_lab_test")
    dr = models.ForeignKey(User,on_delete=models.CASCADE, related_name="dr_lab_test")
    testname =  models.CharField(max_length=200,blank=True,null=True,default="None")
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    paymenttype =  models.CharField(max_length=200,blank=True,null=True,default="None")
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    reporttest =  models.TextField(null=True,blank=True,default="N/A")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Bedcategory(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_bed_category")
    categoryname =  models.CharField(max_length=200,blank=True,null=True,default="None")
    bednumber =  models.CharField(max_length=200,blank=True,null=True,default="None")
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Notice(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_notice")
    title =  models.CharField(max_length=200,blank=True,null=True,default="None")
    noticfor =  models.ForeignKey(Department,on_delete=models.CASCADE, related_name="department_notice")
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Leavetypes(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_leave")
    types = models.CharField(max_length=200,default=0,null=True,blank=True)
    duration = models.CharField(max_length=200,default=0,null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Leave(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_leave_list")
    staff = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_staffs")
    typeofleave =  models.ForeignKey(Leavetypes,on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    reason =  models.TextField(null=True,blank=True,default="N/A")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Chat(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="chat_to_hospital")
    staff = models.ForeignKey(User,on_delete=models.CASCADE,related_name="chat_to_staffs")
    messagesent =  models.TextField(null=True,blank=True,default="N/A")
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    response =  models.TextField(null=True,blank=True,default="N/A")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Childbirth(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_child_birth")
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="patient_who_gave_birth")
    dob = models.DateField()
    firstname = models.CharField(max_length=200,default=0,null=True,blank=True)
    lastname = models.CharField(max_length=200,default=0,null=True,blank=True)
    gender = models.CharField(max_length=200,default=0,null=True,blank=True)
    weight = models.CharField(max_length=200,default=0,null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    remark =  models.TextField(null=True,blank=True,default="N/A")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Deadthrecord(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_child_was_birthed")
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="patient_who_died")
    dod = models.DateField()
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    remark =  models.TextField(null=True,blank=True,default="N/A")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Document(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_who_owns_document")
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="patient_document")
    title = models.CharField(max_length=200,default=0,null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    document = models.ImageField(null=True, upload_to="document/",)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)