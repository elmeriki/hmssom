from django.db import models
from hmmauth.models import *
from customer.models import *


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
    email =  models.EmailField(max_length=200,blank=True,null=True,default="None")
    address =  models.CharField(max_length=200,blank=True,null=True,default="None")
    password =  models.CharField(max_length=200,blank=True,null=True,default="None")
    departmentid =  models.CharField(max_length=200,blank=True,null=True,default="None")
    signature = models.ImageField(null=True, upload_to="doctors_signature/",)
    picture = models.ImageField(null=True, upload_to="doctors_pictures/",)
    profile=  models.TextField(null=True,blank=True)
    message_about_dr=  models.TextField(null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    

# Create your models here.
class Humanresource(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_human_resource")
    category = models.CharField(max_length=200,blank=True,null=True,default="None")
    #employeeid =  models.CharField(max_length=200,blank=True,null=True,default="None")
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
    title =  models.CharField(max_length=200,blank=True,null=True,default="None")
    name =  models.CharField(max_length=200,blank=True,null=True,default="None")
    nok =  models.CharField(max_length=200,blank=True,null=True,default="None")
    non =  models.CharField(max_length=200,blank=True,null=True,default="None")
    phone =  models.CharField(max_length=200,blank=True,null=True,default="None")
    paymenttype =  models.CharField(max_length=200,blank=True,null=True,default="None")
    status =  models.CharField(max_length=200,blank=True,null=True,default="None")
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
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Notice(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_notice")
    title =  models.CharField(max_length=200,blank=True,null=True,default="None")
    noticfor =  models.ForeignKey(Department,on_delete=models.CASCADE, related_name="department_notice")
    noticmsg = models.CharField(max_length=200,default=0,null=True,blank=True)
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
    title = models.CharField(max_length=200,default=0,null=True,blank=True)
    firstname = models.CharField(max_length=200,default=0,null=True,blank=True)
    lastname = models.CharField(max_length=200,default=0,null=True,blank=True)
    race = models.CharField(max_length=200,default=0,null=True,blank=True)
    dob = models.DateField() 
    gender = models.CharField(max_length=200,default=0,null=True,blank=True)
    weight = models.CharField(max_length=200,default=0,null=True,blank=True)
    #status = models.CharField(max_length=200,default=0,null=True,blank=True)
    remark =  models.TextField(null=True,blank=True,default="N/A")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Deadthrecord(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_child_was_birthed")
    title = models.CharField(max_length=200,default=0,null=True,blank=True)
    firstname = models.CharField(max_length=200,default=0,null=True,blank=True)
    lastname = models.CharField(max_length=200,default=0,null=True,blank=True)
    dod = models.DateField()
    gender = models.CharField(max_length=200,default=0,null=True,blank=True)
    race = models.CharField(max_length=200,default=0,null=True,blank=True)
    phone = models.CharField(max_length=200,default=0,null=True,blank=True)
    address = models.CharField(max_length=200,default=0,null=True,blank=True)
    desc = models.CharField(max_length=200,default=0,null=True,blank=True)
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
    
    

class Email(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_email")
    title =  models.CharField(max_length=200,blank=True,null=True,default="None")
    type_sent = models.CharField(max_length=200,default=0,null=True,blank=True)
    message = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class File(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_files")
    title = models.CharField(max_length=200,default=0,null=True,blank=True)
    document = models.ImageField(null=True, upload_to="document/",)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Donor(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_donor")
    title = models.CharField(max_length=200,default=0,null=True,blank=True)
    firstname = models.CharField(max_length=200,default=0,null=True,blank=True)
    lastname = models.CharField(max_length=200,default=0,null=True,blank=True)
    bloodgroup =  models.CharField(max_length=200,blank=True,null=True,default="None")
    weight = models.CharField(max_length=200,default=0,null=True,blank=True)
    age =  models.CharField(max_length=200,blank=True,null=True,default="None")
    gender =  models.CharField(max_length=200,blank=True,null=True,default="None")
    phone =  models.CharField(max_length=200,blank=True,null=True,default="None")
    email =  models.EmailField(max_length=200,blank=True,null=True,default="None")
    lastdonationdate = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Blood(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name="hospital_blood_grou")
    bloodgroup =  models.CharField(max_length=200,blank=True,null=True,default="None")
    quantity = models.CharField(max_length=200,default=0,null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Create your models here.

class Paymentcategory(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,related_name='hospital_category_name')
    category = models.CharField(max_length=200,default=0,null=True,blank=True)
    desc=models.TextField(null=True,blank=True)
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