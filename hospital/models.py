from django.db import models
from hmmauth.models import *
from customer.models import *




# Create your models here.
class Hospital(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_names")
    hospitalid =  models.CharField(max_length=200,blank=True,null=True,default="None")
    package =  models.CharField(max_length=200,blank=True,null=True,default="None")
    desc=models.TextField(null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural ="Hospital"
        
    def __str__(self):
        return self.hospital.first_name
    
    
class Department(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="hospital_diff_departments")
    name =  models.CharField(max_length=200,blank=True,null=True,default="None")
    desc=  models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural ="Department"
        
    def __str__(self):
        return self.hospital.first_name
    
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
    
    class Meta:
        verbose_name_plural ="Doctor"
        
    def __str__(self):
        return self.hospital.first_name

# Create your models here.
class Humanresource(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_human_resource")
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
    
    class Meta:
        verbose_name_plural ="Humanresource"
        
    def __str__(self):
        return self.hospital.first_name

class Patient(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_patient_is_admitted")
    title =  models.CharField(max_length=200,blank=True,null=True,default="None")
    name =  models.CharField(max_length=200,blank=True,null=True,default="None")
    nok =  models.CharField(max_length=200,blank=True,null=True,default="None")
    non =  models.CharField(max_length=200,blank=True,null=True,default="None")
    phone =  models.CharField(max_length=200,blank=True,null=True,default="None")
    paymenttype =  models.CharField(max_length=200,blank=True,null=True,default="None")
    status=models.CharField(max_length=200,blank=True,null=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Patient"
        
    def __str__(self):
        return self.hospital.first_name
    
class Phistory(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,blank=True,null=True,related_name="patient_previous_history")
    title=models.CharField(max_length=200,blank=True,null=True,default="None")
    status=models.CharField(max_length=200,blank=True,null=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Patient History"
        
    def __str__(self):
        return self.patient.name
    
    
class Treatment(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="hospital_patient_treatment_log")
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,blank=True,null=True,related_name="patient_treatment_name")
    dr=models.ForeignKey(Doctor,on_delete=models.CASCADE,blank=True,null=True,related_name="doctor_treatment_log")
    desc =  models.TextField(null=True,blank=True,default="Pending")
    tstatus =models.CharField(max_length=200,default=0,null=True,blank=True)
    remark =  models.TextField(null=True,blank=True,default="Pending")
    dname =  models.TextField(null=True,blank=True,default="Pending")
    pstate = models.CharField(max_length=200,default=0,null=True,blank=True)
    treatmentid =models.CharField(max_length=200,default="Pending",null=True,blank=True)
    payment =models.TextField(null=True,blank=True,default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Treatment Log"
    def __str__(self):
        return self.hospital.first_name

class Labtest(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hostital_lab_test")
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True,related_name="patient_lab_test")
    dr = models.ForeignKey(User,on_delete=models.CASCADE, related_name="dr_lab_test")
    testname =  models.CharField(max_length=200,blank=True,null=True,default="None")
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    paymenttype =  models.CharField(max_length=200,blank=True,null=True,default="None")
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    reporttest =  models.TextField(null=True,blank=True,default="N/A")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Labtest"
        
    def __str__(self):
        return self.hospital.first_name
    
class Bedcategory(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_bed_category")
    categoryname =  models.CharField(max_length=200,blank=True,null=True,default="None")
    bednumber =  models.CharField(max_length=200,blank=True,null=True,default="None")
    price = models.CharField(max_length=200,default=0,null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Bedcategory"
        
    def __str__(self):
        return self.hospital.first_name

class Notices(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_notice")
    title =  models.CharField(max_length=200,blank=True,null=True,default="None")
    noticfor =  models.ForeignKey(Department,on_delete=models.CASCADE,null=True,blank=True, related_name="department_notice")
    noticemsg = models.CharField(max_length=200,default=0,null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Notices"
        
    def __str__(self):
        return self.hospital.first_name
    
class Leavetypes(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_leave")
    types = models.CharField(max_length=200,default=0,null=True,blank=True)
    duration = models.CharField(max_length=200,default=0,null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural ="Leavetypes"
        
    def __str__(self):
        return self.hospital.first_name
    
class Messages(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_customer_messages")
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    names =  models.TextField(null=True,blank=True,default="None")
    phone =  models.TextField(null=True,blank=True,default="None")
    message =  models.TextField(null=True,blank=True,default="None")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Messages"
        
    def __str__(self):
        return self.hospital.first_name
    
class Leave(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_leave_list")
    staff = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_staffs")
    typeofleave =  models.ForeignKey(Leavetypes,on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    reason =  models.TextField(null=True,blank=True,default="N/A")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Leave"
        
    def __str__(self):
        return self.hospital.first_name
    
class Chat(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="chat_to_hospital")
    staff = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="chat_to_staffs")
    messagesent =  models.TextField(null=True,blank=True,default="N/A")
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    response =  models.TextField(null=True,blank=True,default="N/A")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Chat"
        
    def __str__(self):
        return self.hospital.first_name

class Childbirth(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_child_birth")
    title = models.CharField(max_length=200,default=0,null=True,blank=True)
    firstname = models.CharField(max_length=200,default=0,null=True,blank=True)
    lastname = models.CharField(max_length=200,default=0,null=True,blank=True)
    race = models.CharField(max_length=200,default=0,null=True,blank=True)
    dob = models.DateField() 
    gender = models.CharField(max_length=200,default=0,null=True,blank=True)
    weight = models.CharField(max_length=200,default=0,null=True,blank=True)
    remark =  models.TextField(null=True,blank=True,default="N/A")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Childbirth"
        
    def __str__(self):
        return self.hospital.first_name
    
class Deadthrecord(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_child_was_birthed")
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
    class Meta:
        verbose_name_plural ="Deadthrecord"
        
    def __str__(self):
        return self.hospital.first_name
    
class Document(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_who_owns_document")
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="patient_document")
    title = models.CharField(max_length=200,default=0,null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    document = models.ImageField(null=True, upload_to="document/",)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Document"
        
    def __str__(self):
        return self.hospital.first_name
    

class Email(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_email")
    title =  models.CharField(max_length=200,blank=True,null=True,default="None")
    type_sent = models.CharField(max_length=200,default=0,null=True,blank=True)
    message = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Email"
        
    def __str__(self):
        return self.hospital.first_name
    
class File(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_files")
    title = models.CharField(max_length=200,default=0,null=True,blank=True)
    document = models.ImageField(null=True, upload_to="document/",)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural ="File"
        
    def __str__(self):
        return self.hospital.first_name

class Donor(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_donor")
    title = models.CharField(max_length=200,default="",null=True,blank=True)
    firstname = models.CharField(max_length=200,default=0,null=True,blank=True)
    lastname = models.CharField(max_length=200,default=0,null=True,blank=True)
    bloodgroup =  models.CharField(max_length=200,blank=True,null=True,default="")
    weight = models.CharField(max_length=200,default=0,null=True,blank=True)
    age =  models.CharField(max_length=200,blank=True,null=True,default="None")
    gender =  models.CharField(max_length=200,blank=True,null=True,default="None")
    phone =  models.CharField(max_length=200,blank=True,null=True,default="None")
    email =  models.EmailField(max_length=200,blank=True,null=True,default="None")
    quantity = models.CharField(max_length=200,default=0,null=True,blank=True)
    lastdonationdate = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Donor"
        
    def __str__(self):
        return self.hospital.first_name

class Blood(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_blood_grou")
    bloodgroup =  models.CharField(max_length=200,blank=True,null=True,default="")
    quantity = models.CharField(max_length=200,default=0,null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Blood Bank"
        
    def __str__(self):
        return self.hospital.first_name
    
class Bloodfees(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_blood_prices")
    bloodgroup =  models.CharField(max_length=200,blank=True,null=True,default="")
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Blood Bank Price"
        
    def __str__(self):
        return self.hospital.first_name
    
class Bloodpurchase(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="hospital_blood_purchase")
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True,related_name="patient_blood_purchase")
    bloodgroup =  models.CharField(max_length=200,blank=True,null=True,default="")
    amount= models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    quantity = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Blood Purchase"
        
    def __str__(self):
        return self.hospital.first_name

# Create your models here.

class Paymentcategory(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='hospital_category_name')
    category = models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Paymentcategory"
        
    def __str__(self):
        return self.hospital.first_name
    
class Appointmentfees(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='hospital_appointment_fees')
    category = models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Appointment Fees"
        
    def __str__(self):
        return self.hospital.first_name

class Patienttest(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='hospital_patient_test_name')
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True,related_name='patient_test_name')
    category = models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    status=models.CharField(max_length=200,default=0,null=True,blank=True)
    testid = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Patienttest"
        
    def __str__(self):
        return self.hospital.first_name

class Payment(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='payment_category_for_hospital')
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="payment_for_patient")
    category = models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    paymenttype = models.CharField(max_length=200,default=0,null=True,blank=True)
    paymentstatus = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Payment"
        
    def __str__(self):
        return self.hospital.first_name
    
class Expensescategory(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="expenses_for_category")
    name = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural ="Expensescategory"
        
    def __str__(self):
        return self.hospital.first_name
    
class Expense(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="expenses_for_hospital")
    category = models.ForeignKey(Expensescategory,on_delete=models.CASCADE,related_name="expenses_for_categories")
    decs = models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural ="Expense"
        
    def __str__(self):
        return self.hospital.first_name
    
class Lapreport(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="hospital_lap_report")
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,blank=True,null=True,related_name="patient_lap_report")
    status=models.CharField(max_length=200,blank=True,null=True,default="Pending")
    testid = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural ="Lapreport"
        
    def __str__(self):
        return self.hospital.first_name
    
class Labresult(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="hospital_lap_result")
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,blank=True,null=True,related_name="patient_lap_result")
    testname=models.CharField(max_length=200,blank=True,null=True,default="None")
    testreport=models.CharField(max_length=200,blank=True,null=True,default="None")
    testid=models.CharField(max_length=200,blank=True,null=True,default="None")
    status=models.CharField(max_length=200,blank=True,null=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural ="Labresult"
        
    def __str__(self):
        return self.hospital.first_name
    
class Fees(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="hospital_system_fees")
    pakage=models.CharField(max_length=200,blank=True,null=True,default="Pending")
    amount=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    status=models.CharField(max_length=200,blank=True,null=True,default=0)
    paiddate=models.DateField(blank=True,null=True) 
    expireddate=models.DateField(blank=True,null=True) 
    class Meta:
        verbose_name_plural ="Fees"
        
    def __str__(self):
        return self.hospital.first_name
    
class Admission(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="patient_adminited_hospital")
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,blank=True,null=True,related_name="admited_patient")
    dr=models.ForeignKey(Doctor,on_delete=models.CASCADE,blank=True,null=True,related_name="asigned_doctor_to_patient")
    bed=models.ForeignKey(Bedcategory,on_delete=models.CASCADE,blank=True,null=True,related_name="administed_bed")
    diagnosis =models.CharField(max_length=200,default=0,null=True,blank=True)
    phistory =  models.TextField(null=True,blank=True,default="None")
    otherillness =  models.TextField(null=True,blank=True,default="None")
    category =  models.TextField(null=True,blank=True,default="None")
    admitted_date=models.DateField(blank=True,null=True) 
    status=models.CharField(max_length=200,blank=True,null=True,default=0)
    discharge_date=models.DateField(blank=True,null=True) 
    class Meta:
        verbose_name_plural ="Admission Log"
    def __str__(self):
        return self.hospital.first_name
    
class Admissionfees(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="hospital_admision_fees")
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,blank=True,null=True,related_name="patient_admission_fees")
    days=models.CharField(max_length=200,blank=True,null=True,default="0")
    amount=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    paymenttype=models.CharField(max_length=200,blank=True,null=True,default="None")
    status=models.CharField(max_length=200,blank=True,null=True,default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural ="Admissionfees"
        
    def __str__(self):
        return self.hospital.first_name
    
class Assets(models.Model):
    hospital = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="hospital_assets")
    title=models.CharField(max_length=200,blank=True,null=True,default="0")
    amount=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    total=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    quantity=models.CharField(max_length=200,blank=True,null=True,default="None")
    status=models.CharField(max_length=200,blank=True,null=True,default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural ="Assets"
        
    def __str__(self):
        return self.hospital.first_name