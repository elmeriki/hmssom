from django.shortcuts import render
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.models import auth
from django.contrib import  messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Count,Sum
from django.db.models import Q
from django.urls import resolve
import datetime
from datetime import date
from django.core.mail import EmailMessage
import csv
from django.db.models import Q
from django.db import transaction
from django.core.mail import EmailMultiAlternatives
from django.views.generic import View
from hmmauth.models import *
from customer.models import *
from hospital.models import *
from django.db.models import Sum
from random_id import random_id
import string 
import threading


#==================================EMAIL=====================================
class Emailthread(threading.Thread):
    def __init__(self,msg):
        self.msg=msg
        threading.Thread.__init__(self)
    def run(self):
        self.msg.send(fail_silently=False)


#==============================HOSPITAL DASHBOARD==============================
@login_required(login_url='/')  
def hospital_dashboardView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        total_blood_bank_cash=Bloodpurchase.objects.filter(hospital=hospital_instance).filter(created_at__lte=datetime.datetime.today(), created_at__gt=datetime.datetime.today()-datetime.timedelta(days=30)).aggregate(Sum('amount'))['amount__sum']
        total_admission_cash=Admissionfees.objects.filter(hospital=hospital_instance).filter(created_at__lte=datetime.datetime.today(), created_at__gt=datetime.datetime.today()-datetime.timedelta(days=30)).aggregate(Sum('amount'))['amount__sum']
        total_other_cash=Payment.objects.filter(hospital=hospital_instance).filter(created_at__lte=datetime.datetime.today(), created_at__gt=datetime.datetime.today()-datetime.timedelta(days=30)).aggregate(Sum('amount'))['amount__sum']
        total_patient_test_cash=Patienttest.objects.filter(hospital=hospital_instance).filter(created_at__lte=datetime.datetime.today(), created_at__gt=datetime.datetime.today()-datetime.timedelta(days=30)).aggregate(Sum('amount'))['amount__sum']
        total_appointment_cash=Appointment.objects.filter(hospital=hospital_instance).filter(created_at__lte=datetime.datetime.today(), created_at__gt=datetime.datetime.today()-datetime.timedelta(days=30)).aggregate(Sum('amount'))['amount__sum']
        if not total_blood_bank_cash:
            total_blood_bank_cash =0
        if not total_admission_cash:
            total_admission_cash=0
        if not total_other_cash:
            total_other_cash=0
        if not total_patient_test_cash:
            total_patient_test_cash=0
        if not total_appointment_cash:
            total_appointment_cash=0
        
        total = total_blood_bank_cash + total_admission_cash + total_other_cash + total_patient_test_cash + total_appointment_cash
        data = {
        'count_number_of_patient':Patient.objects.filter(hospital=hospital_instance).count(),
        'count_number_of_doctors':Doctor.objects.filter(hospital=hospital_instance).count(),
        'count_number_of_appointment':Appointment.objects.filter(hospital=hospital_instance,status=0).count(),
        'doctor_list':Doctor.objects.filter(hospital=hospital_instance),
        'patient_list':Patient.objects.filter(hospital=hospital_instance)[:10],
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        'licence_date_instance':Fees.objects.filter(hospital=hospital_instance,status=1),
        'hospital_instance':hospital_instance,
        'total': total
        }
        return render(request,'hospital/dashboard.html',context=data)
    
#====================================DEPARTMENT==================================
@login_required(login_url='/')  
def departmentView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        hospital_department=Department.objects.filter(hospital=hospital_instance)
        data = {
        'hospital_department':hospital_department,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/department.html',context=data)
    
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        hospital_department=Department.objects.filter(hospital=hospital_instance)
        data = {
        'hospital_department':hospital_department,
        'reception_instance_to_display_profile_picture':recep_instance,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'receptionist/department.html',context=data)
    
    
@login_required(login_url='/')  
def add_departmentView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/add_department.html',context=data)

    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'receptionist/add_department.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def save_add_departmentView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        department_name = request.POST['departmentname']
        departmentdesc = request.POST['departmentdesc']
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        create_Department =Department(hospital=hospital_instance,name=department_name,desc=departmentdesc)
        if create_Department:
            create_Department.save()
            messages.info(request,'Department Created successfully')
            return redirect('/add_department')
        else:
            return redirect('/department')
        
    if request.user.is_authenticated and request.user.is_rep and request.method=="POST":
        department_name = request.POST['departmentname']
        departmentdesc = request.POST['departmentdesc']
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        create_Department =Department(hospital=hospital_instance,name=department_name,desc=departmentdesc)
        if create_Department:
            create_Department.save()
            messages.info(request,'Department Created successfully')
            return redirect('/add_department')
        else:
            return redirect('/department')
    else:
       return redirect('/department')
    

@login_required(login_url='/')  
def edit_departmentView(request,departmentid):
    if request.user.is_authenticated and request.user.is_hospital:
        get_department_instance = Department.objects.get(id=departmentid)
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
        'department':get_department_instance.name,
        'departmentdesc':get_department_instance.desc,
        'departmentid':get_department_instance.id,
        'departmentid':departmentid,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/edit_department.html',context=data)
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        get_department_instance=Department.objects.get(id=departmentid)
        data = {
        'department':get_department_instance.name,
        'departmentdesc':get_department_instance.desc,
        'departmentid':get_department_instance.id,
        'departmentid':departmentid,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'receptionist/edit_department.html',context=data)

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_departmentView(request,departmentid):
    if request.user.is_authenticated and request.user.is_hospital:
        departmentname=request.POST['departmentname']
        departmentdesc=request.POST['departmentdesc']
        Department.objects.filter(pk=departmentid).update(name=departmentname)
        Department.objects.filter(pk=departmentid).update(desc=departmentdesc)
        messages.info(request,'Update has been done successfully')
        return redirect(f'/edit_department/{departmentid}')
    if request.user.is_authenticated and request.user.is_rep:
        departmentname=request.POST['departmentname']
        departmentdesc=request.POST['departmentdesc']
        Department.objects.filter(pk=departmentid).update(name=departmentname)
        Department.objects.filter(pk=departmentid).update(desc=departmentdesc)
        messages.info(request,'Update has been done successfully')
        return redirect(f'/edit_department/{departmentid}')

@login_required(login_url='/')  
def delete_departmentView(request, departmentid):
    if request.user.is_authenticated and request.user.is_hospital:
        delete_department = Department.objects.get(id=departmentid)
        delete_department.delete()
        return redirect('/department')
    if request.user.is_authenticated and request.user.is_rep:
        delete_department = Department.objects.get(id=departmentid)
        delete_department.delete()
        return redirect('/department')

#=======================================DOCTOR====================================
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_doctorView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
        hospital_email_address = request.user.email
        hospital_instance=User.objects.get(username=username)
        if len(request.FILES) != 0:
            picture=request.FILES['picture']
            signature=request.FILES['signature']
            picturefilesize=picture.size
            signaturefilesize=signature.size
            if picturefilesize > 2621440 and signaturefilesize > 2621440:
                messages.info(request,"The Dr Picture and Signature is Biger Than 2MB")
                return redirect('/add_doctor')
        if User.objects.filter(email=request.POST['email']).exists():
            messages.info(request,"The Email address is used already")
            return redirect('/add_doctor')
        name = request.POST['name']
        type = request.POST['type']
        email = request.POST['email']
        number = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        departmentid = request.POST['department']
        message_about_dr = request.POST['message_about_dr']
        doctorsid = random_id(length=9,character_set=string.digits)
        department_instance = Department.objects.get(id=departmentid)
        if type == "Dr":
            create_new_doctors_account=User.objects.create_user(username=email,first_name=name,is_activation=True,last_name=name,password=password,is_dr=True,email=email,address=address,number=number,customerid=doctorsid,hospital_id=hospital_email_address)
            create_new_doctors_account.save()
            save_doctors_details=Doctor(user=create_new_doctors_account,hospital=hospital_instance,department=department_instance,name=name,email=email,phone=number,address=address,signature=signature,picture=picture,message_about_dr=message_about_dr)
            save_doctors_details.save()
            messages.info(request,'Doctors Profile has been created successfully')
            return render(request,'hospital/add_doctor.html',{})
        elif type == "Lab":
            create_new_doctors_account=User.objects.create_user(username=email,first_name=name,is_activation=True,last_name=name,password=password,is_lab=True,email=email,address=address,number=number,customerid=doctorsid,hospital_id=hospital_email_address)
            create_new_doctors_account.save()
            save_doctors_details=Doctor(user=create_new_doctors_account,hospital=hospital_instance,department=department_instance,name=name,email=email,phone=number,address=address,signature=signature,picture=picture,message_about_dr=message_about_dr)
            save_doctors_details.save()
            messages.info(request,'Laboratory Profile has been created successfully')
            return render(request,'hospital/add_doctor.html',{}) 
        elif type == "Rep":
            create_new_doctors_account=User.objects.create_user(username=email,first_name=name,is_activation=True,last_name=name,password=password,is_rep=True,email=email,address=address,number=number,customerid=doctorsid,hospital_id=hospital_email_address)
            create_new_doctors_account.save()
            save_doctors_details=Doctor(user=create_new_doctors_account,hospital=hospital_instance,department=department_instance,name=name,email=email,phone=number,address=address,signature=signature,picture=picture,message_about_dr=message_about_dr)
            save_doctors_details.save()
            messages.info(request,'Receptionist Profile has been created successfully')
            return render(request,'hospital/add_doctor.html',{}) 
        elif type == "Pha":
            create_new_doctors_account=User.objects.create_user(username=email,first_name=name,is_activation=True,last_name=name,password=password,is_pha=True,email=email,address=address,number=number,customerid=doctorsid,hospital_id=hospital_email_address)
            create_new_doctors_account.save()
            save_doctors_details=Doctor(user=create_new_doctors_account,hospital=hospital_instance,department=department_instance,name=name,email=email,phone=number,address=address,signature=signature,picture=picture,message_about_dr=message_about_dr)
            save_doctors_details.save()
            messages.info(request,'Phamarcist Profile has been created successfully')
            return render(request,'hospital/add_doctor.html',{}) 

    
@login_required(login_url='/')  
def add_doctorView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        get_all_hospital_department_list = Department.objects.filter(hospital=hospital_instance)
        data = {
            'get_all_hospital_department_list':get_all_hospital_department_list,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/add_doctor.html',context=data)
    
    
@login_required(login_url='/')  
def add_adminView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        get_all_hospital_department_list = Department.objects.filter(hospital=hospital_instance)
        data = {
            'get_all_hospital_department_list':get_all_hospital_department_list,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/add_doctor.html',context=data)
    

@login_required(login_url='/')  
def doctor_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        hospital_doctor =Doctor.objects.filter(hospital=hospital_instance)
        data = {
            'hospital_doctor':hospital_doctor,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/doctor_list.html',context=data)

@login_required(login_url='/')  
def administrator_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
            'administrator_list':Doctor.objects.filter(hospital=hospital_instance),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/administrator_list.html',context=data)

@login_required(login_url='/')  
def edit_doctorView(request,doctorsid):
    if request.user.is_authenticated and request.user.is_hospital:
        get_doctor_instance = Doctor.objects.get(id=doctorsid)
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
        'name' : get_doctor_instance.name,
        'email' : get_doctor_instance.email,
        'phone' : get_doctor_instance.phone,
        'address' : get_doctor_instance.address,
        'department' : get_doctor_instance.department,
        'password' : get_doctor_instance.user.password,
        'message_about_dr': get_doctor_instance.message_about_dr,
        'status' : get_doctor_instance.status,
        'picture' : get_doctor_instance.picture,
        'signature' : get_doctor_instance.signature,
        'doctorsid':get_doctor_instance.id,
        'doctorsid':doctorsid,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/edit_doctor.html',context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_doctorView(request,doctorsid):
    if request.user.is_authenticated and request.user.is_hospital:
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        department = request.POST['department']
        message_about_dr = request.POST['message_about_dr']
        status = request.POST['status']
        picture = request.POST['picture']
        signature = request.POST['signature']

        
        Doctor.objects.filter(pk=doctorsid).update(name=name)
        Doctor.objects.filter(pk=doctorsid).update(email=email)
        Doctor.objects.filter(pk=doctorsid).update(phone=phone)
        Doctor.objects.filter(pk=doctorsid).update(address=address)
        Doctor.objects.filter(pk=doctorsid).update(password=password)
        Doctor.objects.filter(pk=doctorsid).update(departmentid=department)
        Doctor.objects.filter(pk=doctorsid).update(message_about_dr=message_about_dr)
        Doctor.objects.filter(pk=doctorsid).update(status=status)
        Doctor.objects.filter(pk=doctorsid).update(picture=picture)
        Doctor.objects.filter(pk=doctorsid).update(signature=signature)
        messages.info(request,'Update has been done successfully')

        return redirect(f'/edit_doctor/{doctorsid}')


@login_required(login_url='/')  
def delete_doctorView(request, doctorsid):
    if request.user.is_authenticated and request.user.is_hospital:
        delete_doctor = Doctor.objects.get(id=doctorsid)
        delete_doctor.delete()
        return redirect('/doctor_list')
    

@login_required(login_url='/')  
def doctor_treatment_recordView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
            'hospital_doctor_treatment_log':Treatment.objects.filter(hospital=hospital_instance,pstate="Treated")[:20],
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
    return render(request,'hospital/doctor_treatment_record.html',context=data)

@login_required(login_url='/')  
def doctor_visitView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),  
        }
        return render(request,'hospital/doctor_visit.html',context=data)


@login_required(login_url='/')  
def add_doctor_visitView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),  
        }
        return render(request,'hospital/add_doctor_visit.html',context=data)


#===========================================PATIENT========================================
@login_required(login_url='/')  
def add_patientView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),  
        }
        return render(request,'hospital/add_patient.html',context=data)
    
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),  
        }
        return render(request,'receptionist/add_patient.html',context=data)
    
@login_required(login_url='/')  
def add_patient_historyView(request,patient_id):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'patient_id':patient_id,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),  
        }
        return render(request,'hospital/add_patient_history.html',context=data)
    
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'patient_id':patient_id,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'receptionist/add_patient_history.html',context=data)

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def save_add_patientView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        title = request.POST['title']
        patientname = request.POST['patientname']
        nok = request.POST['nok']
        non = request.POST['non']
        phone = request.POST['phone']        
        paymenttype = request.POST['paymenttype']
        status = request.POST['status']
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        if Patient.objects.filter(hospital=hospital_instance,phone=phone).exists():
            messages.info(request,'Patient Number already used')
            return redirect('/add_patient')
        
        if Patient.objects.filter(hospital=hospital_instance,non=non).exists():
            messages.info(request,'Next of king Number already used')
            return redirect('/add_patient')
        
        create_patient=Patient(hospital=hospital_instance,title=title,name=patientname,nok=nok,non=non,phone=phone,paymenttype=paymenttype,status=status)
        if create_patient:
            create_patient.save()
            messages.info(request,'Patient Created successfully')
            return redirect('/add_patient')
        else:
            return redirect('/patient_list')
    if request.user.is_authenticated and request.user.is_rep and request.method=="POST":
        title = request.POST['title']
        patientname = request.POST['patientname']
        nok = request.POST['nok']
        non = request.POST['non']
        phone = request.POST['phone']        
        paymenttype = request.POST['paymenttype']
        status = request.POST['status']
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username) 
        if Patient.objects.filter(hospital=hospital_instance,phone=phone).exists():
            messages.info(request,'Patient Number already used')
            return redirect('/add_patient')
        
        if Patient.objects.filter(hospital=hospital_instance,non=non).exists():
            messages.info(request,'Next of king Number already used')
            return redirect('/add_patient')
        
        create_patient=Patient(hospital=hospital_instance,title=title,name=patientname,nok=nok,non=non,phone=phone,paymenttype=paymenttype,status=status)
        if create_patient:
            create_patient.save()
            messages.info(request,'Patient Created successfully')
            return redirect('/add_patient')
        else:
            return redirect('/patient_list')
    else:
       return redirect('/patient_list')
    


@login_required(login_url='/')  
def patient_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        hospital_patient =Patient.objects.filter(hospital=hospital_instance)
        data = {
        'hospital_patient':hospital_patient,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'hospital/patient_list.html',context=data)    
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        hospital_patient =Patient.objects.filter(hospital=hospital_instance)
        data = {
        'hospital_patient':hospital_patient,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'receptionist/patient_list.html',context=data)    


@login_required(login_url='/')  
def edit_patientView(request,patientid):
    if request.user.is_authenticated and request.user.is_hospital:
        get_patient_instance = Patient.objects.get(id=patientid)
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
        'title':get_patient_instance.title,
        'patientname':get_patient_instance.name,
        'nok':get_patient_instance.nok,
        'non':get_patient_instance.non,
        'phone':get_patient_instance.phone,
        'paymenttype':get_patient_instance.paymenttype,
        'status':get_patient_instance.status,
        'patientid':get_patient_instance.id,
        'patientid':patientid,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'hospital/edit_patient.html',context=data)
    
    if request.user.is_authenticated and request.user.is_rep:
        get_patient_instance = Patient.objects.get(id=patientid)
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
        'title':get_patient_instance.title,
        'patientname':get_patient_instance.name,
        'nok':get_patient_instance.nok,
        'non':get_patient_instance.non,
        'phone':get_patient_instance.phone,
        'paymenttype':get_patient_instance.paymenttype,
        'status':get_patient_instance.status,
        'patientid':get_patient_instance.id,
        'patientid':patientid,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'receptionist/edit_patient.html',context=data)
    

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_patientView(request,patientid):
    if request.user.is_authenticated and request.user.is_hospital:
        title = request.POST['title']
        patientname = request.POST['patientname']
        nok = request.POST['nok']
        non = request.POST['non']
        phone = request.POST['phone']        
        paymenttype = request.POST['paymenttype']
        status = request.POST['status']        
        Patient.objects.filter(pk=patientid).update(title=title)
        Patient.objects.filter(pk=patientid).update(name=patientname)
        Patient.objects.filter(pk=patientid).update(nok=nok)
        Patient.objects.filter(pk=patientid).update(non=non)
        Patient.objects.filter(pk=patientid).update(phone=phone)
        Patient.objects.filter(pk=patientid).update(paymenttype=paymenttype)
        Patient.objects.filter(pk=patientid).update(status=status)
        messages.info(request,'Update has been done successfully')
        return redirect(f'/edit_patient/{patientid}')
    if request.user.is_authenticated and request.user.is_rep:
        title = request.POST['title']
        patientname = request.POST['patientname']
        nok = request.POST['nok']
        non = request.POST['non']
        phone = request.POST['phone']        
        paymenttype = request.POST['paymenttype']
        status = request.POST['status']        
        Patient.objects.filter(pk=patientid).update(title=title)
        Patient.objects.filter(pk=patientid).update(name=patientname)
        Patient.objects.filter(pk=patientid).update(nok=nok)
        Patient.objects.filter(pk=patientid).update(non=non)
        Patient.objects.filter(pk=patientid).update(phone=phone)
        Patient.objects.filter(pk=patientid).update(paymenttype=paymenttype)
        Patient.objects.filter(pk=patientid).update(status=status)
        messages.info(request,'Update has been done successfully')
        return redirect(f'/edit_patient/{patientid}')

@login_required(login_url='/')  
def delete_patientView(request, patientid):
    if request.user.is_authenticated and request.user.is_hospital:
        delete_patient = Patient.objects.get(id=patientid)
        delete_patient.delete()
        return redirect('/patient_list')
    if request.user.is_authenticated and request.user.is_rep:
        delete_patient = Patient.objects.get(id=patientid)
        delete_patient.delete()
        return redirect('/patient_list')

@login_required(login_url='/')  
def patient_paymentsView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'hospital/patient_payments.html',context=data) 


@login_required(login_url='/')  
def patient_payment_historyView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'hospital/patient_payment_history.html',context=data) 

@login_required(login_url='/')  
def case_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'hospital/case_list.html',context=data) 


@login_required(login_url='/')  
def add_caseView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'hospital/add_case.html',context=data) 


@login_required(login_url='/')  
def document_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'hospital/document_list.html',context=data) 
    
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'receptionist/document_list.html') 

@login_required(login_url='/')  
def add_documentView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'hospital/add_document.html',context=data) 
    
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'receptionist/add_document.html',context=data) 
    



#===========================================HOSPITAL PROFILE========================================
@login_required(login_url='/')  
def hospital_profileView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        about_the_hospital_text=Hospital.objects.get(hospital=hospital_instance)
        data = {
        'count_number_of_patient':Patient.objects.filter(hospital=hospital_instance).count(),
        'count_number_of_doctors':Doctor.objects.filter(hospital=hospital_instance).count(),
        'about_the_hospital_text':about_the_hospital_text.desc,
        'count_number_of_appointment':Appointment.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'hospital/profile.html',context=data)
    
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        about_the_hospital_text=Hospital.objects.get(hospital=hospital_instance)

        data = {
        'count_number_of_patient':Patient.objects.filter(hospital=hospital_instance).count(),
        'count_number_of_doctors':Doctor.objects.filter(hospital=hospital_instance).count(),
        'about_the_hospital_text':about_the_hospital_text.desc,
        'count_number_of_appointment':Appointment.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'receptionist/profile.html',context=data)
    
    if request.user.is_authenticated and request.user.is_lab:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        lab_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=lab_instance.hospital.username)
        about_the_hospital_text=Hospital.objects.get(hospital=hospital_instance)

        data = {
        'count_number_of_patient':Patient.objects.filter(hospital=hospital_instance).count(),
        'count_number_of_doctors':Doctor.objects.filter(hospital=hospital_instance).count(),
        'about_the_hospital_text':about_the_hospital_text.desc,
        'count_number_of_appointment':Appointment.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'laboratory/profile.html',context=data)
    

@login_required(login_url='/')  
def doctor_profileView(request):
    if request.user.is_authenticated and request.user.is_dr:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'doctor/profile.html',context=data)
    
    
@login_required(login_url='/')  
def lab_profileView(request):
    if request.user.is_authenticated and request.user.is_lab:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'laboratory/profile.html',context=data)


#===========================================EMAIL========================================
@login_required(login_url='/')  
def compose_emailView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        sent_email_count = Email.objects.filter(hospital=hospital_instance).count()
        data = {
        'sent_email_count':sent_email_count,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'hospital/compose.html',context=data)
    
    
@login_required(login_url='/')  
def email_inboxView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        sent_email_count=Email.objects.filter(hospital=hospital_instance).count()
        sent_email=Email.objects.filter(hospital=hospital_instance)
        data = {
            'sent_email_count':sent_email_count,
            'sent_email':sent_email,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'hospital/inbox.html',context=data)
    

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def send_bulk_emailView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        category = request.POST['category']
        title = request.POST['title']
        message = request.POST['text']
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        if category == "Doctor" or category == "Laboratorist":
            if not Doctor.objects.filter(hospital=hospital_instance):
                messages.info(request,'No Email Found')
                return redirect('/compose_email')
            if Doctor.objects.filter(hospital=hospital_instance):
                fetch_all_staff_email=Doctor.objects.filter(hospital=hospital_instance)
                for each_staff_info in fetch_all_staff_email:
                    subject=title
                    from_email=f'{each_staff_info.hospital.first_name} <no_reply@hmssom.com>'
                    sento = each_staff_info.email
                    messagbody = '#'
                    html_content =f'''<p><strong>Dear {each_staff_info.name} </strong> <br><br>  
                    {message}
                    <br><hr> Best Regards <br> {each_staff_info.hospital.first_name} </p>'''
                    msg=EmailMultiAlternatives(subject, messagbody, from_email,[sento])
                    msg.attach_alternative(html_content, "text/html")
                    Emailthread(msg).start()
            save_sent_email=Email(hospital=hospital_instance,title=title,message=message)
            if save_sent_email:
                save_sent_email.save()
                if category == "Doctor":
                    messages.info(request,'Email sent successfully to all Doctors') 
                    return redirect('/compose_email')
                if category == "Laboratorist": 
                    messages.info(request,'Email sent successfully to all Laboratorist') 
                    return redirect('/compose_email')
        if category == "Nurse" or category == "Accountant" or category == "Receptionist":
            if not Humanresource.objects.filter(hospital=hospital_instance):
                messages.info(request,'No Email Found')
                return redirect('/compose_email')
            if Humanresource.objects.filter(hospital=hospital_instance):
                fetch_all_staff_email=Humanresource.objects.filter(hospital=hospital_instance)
                for each_staff_info in fetch_all_staff_email:
                    subject=title
                    from_email=f'{each_staff_info.hospital.first_name} <no_reply@hmssom.com>'
                    sento = each_staff_info.email
                    messagbody = '#'
                    html_content =f'''<p><strong>Dear {each_staff_info.name} </strong> <br><br>  
                    {message}
                    <br><hr> Best Regards <br> {each_staff_info.hospital.first_name} </p>'''
                    msg=EmailMultiAlternatives(subject, messagbody, from_email,[sento])
                    msg.attach_alternative(html_content, "text/html")
                    Emailthread(msg).start()
            save_sent_email=Email(hospital=hospital_instance,title=title,message=message)
            if save_sent_email:
                save_sent_email.save()
                if category == "Nurse":
                    messages.info(request,'Email sent successfully to all Nurses') 
                    return redirect('/compose_email')
                if category == "Accountant":
                    messages.info(request,'Email sent successfully to all Accountants') 
                    return redirect('/compose_email')
                if category == "Receptionist":
                    messages.info(request,'Email sent successfully to all Receptionist') 
                    return redirect('/compose_email')
        else:
            messages.info(request,'Something went wrong while sending email') 
            return redirect('/compose_email')
        

 #===========================================HUMAN RESOURCES========================================       
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_humanresourceView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
        if len(request.FILES) != 0:
            picture=request.FILES['picture']
            signature=request.FILES['signature']
            picturefilesize=picture.size
            signaturefilesize=signature.size
            if picturefilesize > 2621440 and signaturefilesize > 2621440:
                messages.info(request,"The Employee Picture and Signature is Biger Than 2MB")
                return redirect('/add_humanresource')
        if User.objects.filter(email=request.POST['email']).exists():
            messages.info(request,"The Email address is used already")
            return redirect('/add_humanresource')
        hospital_instance=User.objects.get(username=username)
        category = request.POST['category']
        title = request.POST['title']
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']   
        # picture = request.POST['picture']
        # signature = request.POST['signature']     
       # humanresourceid = random_id(length=10,character_set=string.digits)
        hospital_instance=User.objects.get(username=username)
        create_Humanresource=Humanresource(hospital=hospital_instance, category=category,title=title,name=name,email=email,address=address,phone=phone,signature=signature,picture=picture)
        if create_Humanresource:
            create_Humanresource.save()
            messages.info(request,'Employee Created successfully')
            return redirect('/add_humanresource')
        else:
            return redirect('/humanresource_list')
    else:
       return redirect('/humanresource_list')



@login_required(login_url='/')  
def add_humanresourceView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'hospital/add_humanresource.html',context=data)
    
    
def humanresource_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        list_all_humanresource=Humanresource.objects.filter(hospital=hospital_instance)
        hr_data = {
            'list_all_humanresource':list_all_humanresource,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/humanresource_list.html',context=hr_data)
    
@login_required(login_url='/')  
def edit_humanresourceView(request,humanresourceid):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        get_humanresource_instance = Humanresource.objects.get(id=humanresourceid)
        data = {
        'category' : get_humanresource_instance.category,
        'title' : get_humanresource_instance.title,
        'name' : get_humanresource_instance.name,
        'email' : get_humanresource_instance.email,
        'phone' : get_humanresource_instance.phone,
        'address' : get_humanresource_instance.address,
        'picture' : get_humanresource_instance.picture,
        'signature' : get_humanresource_instance.signature,
        'humanresourceid':get_humanresource_instance.id,
        'humanresourceid':humanresourceid,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/edit_humanresource.html',context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_humanresourceView(request,humanresourceid):
    if request.user.is_authenticated and request.user.is_hospital:
        category = request.POST['category']
        title = request.POST['title']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        picture = request.POST['picture']
        signature = request.POST['signature']


        Humanresource.objects.filter(pk=humanresourceid).update(category=category)
        Humanresource.objects.filter(pk=humanresourceid).update(title=title)
        Humanresource.objects.filter(pk=humanresourceid).update(name=name)
        Humanresource.objects.filter(pk=humanresourceid).update(email=email)
        Humanresource.objects.filter(pk=humanresourceid).update(phone=phone)
        Humanresource.objects.filter(pk=humanresourceid).update(address=address)
        Humanresource.objects.filter(pk=humanresourceid).update(picture=picture)
        Humanresource.objects.filter(pk=humanresourceid).update(signature=signature)
        messages.info(request,'Update has been done successfully')

        return redirect(f'/edit_humanresource/{humanresourceid}')


@login_required(login_url='/')  
def delete_humanresourceView(request, humanresourceid):
    if request.user.is_authenticated and request.user.is_hospital:
        delete_humanresource = Humanresource.objects.get(id=humanresourceid)
        delete_humanresource.delete()
        return redirect('/humanresource_list')
    
    
def humanresource_by_categoryView(request,category):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        if category == "Doctor":
            list_all_doctor=Humanresource.objects.filter(hospital=hospital_instance,category=category)
            data = {
                'list_all_doctor':list_all_doctor,
                'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
               'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
            }
            return render(request,'hospital/humanresource_list.html',context=data)
        if category == "Nurse":
            list_all_nurses=Humanresource.objects.filter(hospital=hospital_instance,category=category)
            data = {
                'list_all_nurses':list_all_nurses,
                'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
                'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
            }
            return render(request,'hospital/humanresource_list.html',context=data)
        
        if category == "Phamarcist":
            list_all_phamarcist=Humanresource.objects.filter(hospital=hospital_instance,category=category)
            data = {
                'list_all_phamarcist':list_all_phamarcist,
                'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
                'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
            }
            return render(request,'hospital/humanresource_list.html',context=data)
        if category == "Laboratorist":
            list_all_laboratorist=Humanresource.objects.filter(hospital=hospital_instance,category=category)
            data = {
                'list_all_laboratorist':list_all_laboratorist,
                'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
                'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
            }
            return render(request,'hospital/humanresource_list.html',context=data)
        
        if category == "Accountant":
            list_all_accountant=Humanresource.objects.filter(hospital=hospital_instance,category=category)
            data = {
                'list_all_accountant':list_all_accountant,
                'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
                'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
            }
            return render(request,'hospital/humanresource_list.html',context=data)
        
        if category == "Receptionist":
            list_all_receptionist=Humanresource.objects.filter(hospital=hospital_instance,category=category)
            data = {
                'list_all_receptionist':list_all_receptionist,
                'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
               'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
            }
            return render(request,'hospital/humanresource_list.html',context=data)
        

#===========================================BED CATEGORY========================================
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_bedcategoryView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        return render(request,'hospital/add_bedcategory.html')

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def bed_admissionView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
            'bed_list':Bedcategory.objects.filter(hospital=hospital_instance,status="Available"),
            'doctor_list':Doctor.objects.filter(hospital=hospital_instance),
            'hospital_instance':hospital_instance,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/bed_admission.html',context=data)
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username) 
        data = {
            'bed_list':Bedcategory.objects.filter(hospital=hospital_instance,status="Available"),
            'doctor_list':Doctor.objects.filter(hospital=hospital_instance),
            'hospital_instance':hospital_instance,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'receptionist/bed_admission.html',context=data)
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_admissionView(request):
    if request.user.is_authenticated and request.user.is_hospital or request.user.is_rep and request.method=="POST":
        bed_id=request.POST['bed']
        patientid=request.POST['patientid']
        doctor_email=request.POST['doctor']
        diagnosis=request.POST['diagnosis']
        admission_date=request.POST['admission_date']
        phistory=request.POST['phistory']
        otherillness=request.POST['otherillness']
        category=request.POST['category']
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(email=doctor_email)
        bed_instance=Bedcategory.objects.get(id=bed_id)
        patient_instance=Patient.objects.get(phone=patientid)
        if Admission.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(status=0):
            messages.info(request,'Previous admission has to be close before you can book another')
            return redirect('/bed_admission')
        else:
            create_patient_admission=Admission(hospital=hospital_instance,patient=patient_instance,dr=doctor_instance,bed=bed_instance,diagnosis=diagnosis,phistory=phistory,otherillness=otherillness,category=category,admitted_date=admission_date)
            if create_patient_admission:
                create_patient_admission.save()
                Bedcategory.objects.filter(id=bed_id).update(status="Unavailable")
                return redirect('/bed_admission')
    else:
        return redirect('/bed_admission')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_bedcategoryView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        categoryname = request.POST['categoryname']
        bednumber = request.POST['bednumber']
        status = request.POST['status'] 
        amount = request.POST['amount']            
        id = random_id(length=9,character_set=string.digits)
        save_bedcategory_details=Bedcategory(hospital=hospital_instance, id=id, categoryname=categoryname,bednumber=bednumber,status=status,price=amount)
        save_bedcategory_details.save()
        messages.info(request,'Bed Category created successfully')
        return redirect('/add_bedcategory')
    
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def save_patient_historyView(request,patient_id):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        patient_instance=Patient.objects.get(id=patient_id)
        patient_history = request.POST['patient_history']
        save_patient_history=Phistory(patient=patient_instance,title=patient_history)
        save_patient_history.save()
        messages.info(request,'Patient History added successfully')
        return redirect(f'/add_patient_history/{patient_id}')
    
    if request.user.is_authenticated and request.user.is_rep and request.method=="POST":
        patient_instance=Patient.objects.get(id=patient_id)
        patient_history = request.POST['patient_history']
        save_patient_history=Phistory(patient=patient_instance,title=patient_history)
        save_patient_history.save()
        messages.info(request,'Patient History added successfully')
        return redirect(f'/add_patient_history/{patient_id}')

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def bedcategory_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        list_all_bedcategories=Bedcategory.objects.filter(hospital=hospital_instance)
        bedcategory_data = {
            'list_all_bedcategories':list_all_bedcategories,
            'hospital_instance':hospital_instance,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/bedcategory_list.html',context=bedcategory_data)
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def all_admissionView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        list_all_admission=Admission.objects.filter(hospital=hospital_instance)
        bedcategory_data = {
            'list_all_admission':list_all_admission,
            'hospital_instance':hospital_instance,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/all_admission.html',context=bedcategory_data)
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username) 
        list_all_admission=Admission.objects.filter(hospital=hospital_instance)
        bedcategory_data = {
            'list_all_admission':list_all_admission,
            'hospital_instance':hospital_instance,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'receptionist/all_admission.html',context=bedcategory_data)
    

@login_required(login_url='/')  
def edit_bedcategoryView(request,bedcategoryid):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        get_bedcategory_instance = Bedcategory.objects.get(id=bedcategoryid)
        data = {
        'categoryname':get_bedcategory_instance.categoryname,
        'bednumber':get_bedcategory_instance.bednumber,
        'status':get_bedcategory_instance.status,
        'bedcategoryid':get_bedcategory_instance.id,
        'bedcategoryid':bedcategoryid,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/edit_bedcategory.html',context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_bedcategoryView(request,bedcategoryid):
    if request.user.is_authenticated and request.user.is_hospital:
        categoryname = request.POST['categoryname']
        bednumber = request.POST['bednumber']
        status = request.POST['status']  
        Bedcategory.objects.filter(pk=bedcategoryid).update(categoryname=categoryname)
        Bedcategory.objects.filter(pk=bedcategoryid).update(bednumber=bednumber)
        Bedcategory.objects.filter(pk=bedcategoryid).update(status=status)
        messages.info(request,'Update has been done successfully')
        return redirect(f'/edit_bedcategory/{bedcategoryid}')


@login_required(login_url='/')  
def delete_bedcategoryView(request, bedcategoryid):
    if request.user.is_authenticated and request.user.is_hospital:
        delete_bedcategory = Bedcategory.objects.get(id=bedcategoryid)
        delete_bedcategory.delete()
        return redirect('/bedcategory_list')
    
    

#===========================================CHILD BIRTH========================================
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_childbirthView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        title = request.POST['title']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        dob = request.POST['dob'] 
        gender = request.POST['gender']  
        weight = request.POST['weight']
        race = request.POST['race']
        remark = request.POST['remark']
             
        id = random_id(length=9,character_set=string.digits)
    
        save_childbirth_details=Childbirth(hospital=hospital_instance, id=id, title=title,firstname=firstname, lastname=lastname,
                                            dob=dob, gender=gender,weight=weight, race=race, remark=remark)
        save_childbirth_details.save()
                                             
        messages.info(request,'Child birth record created successfully')
        return redirect('/add_childbirth')
    if request.user.is_authenticated and request.user.is_rep and request.method=="POST":
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        title = request.POST['title']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        dob = request.POST['dob'] 
        gender = request.POST['gender']  
        weight = request.POST['weight']
        race = request.POST['race']
        remark = request.POST['remark']
             
        id = random_id(length=9,character_set=string.digits)
    
        save_childbirth_details=Childbirth(hospital=hospital_instance, id=id, title=title,firstname=firstname, lastname=lastname,
                                            dob=dob, gender=gender,weight=weight, race=race, remark=remark)
        save_childbirth_details.save()
                                             
        messages.info(request,'Child birth record created successfully')
        return redirect('/add_childbirth')
    
       
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_childbirthView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        return render(request,'hospital/add_childbirth.html')
    
    if request.user.is_authenticated and request.user.is_rep:
        return render(request,'receptionist/add_childbirth.html')

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def childbirth_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        list_all_childbirth=Childbirth.objects.filter(hospital=hospital_instance)
        childbirth_data = {
            'list_all_childbirth':list_all_childbirth,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
           'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/childbirth_list.html',context=childbirth_data)
    
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        list_all_childbirth=Childbirth.objects.filter(hospital=hospital_instance)
        childbirth_data = {
            'list_all_childbirth':list_all_childbirth,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'receptionist/childbirth_list.html',context=childbirth_data)
    
@login_required(login_url='/')  
def edit_childbirthView(request,childbirth_id):
    if request.user.is_authenticated and request.user.is_hospital:
        get_childbirth_instance = Childbirth.objects.get(id=childbirth_id)
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = { 
        'title':get_childbirth_instance.title,
        'firstname':get_childbirth_instance.firstname,
        'lastname':get_childbirth_instance.lastname,
        'dob':get_childbirth_instance.dob,
        'gender':get_childbirth_instance.gender,
        'weight':get_childbirth_instance.weight,
        'race':get_childbirth_instance.race,
        'remark':get_childbirth_instance.remark,
        'childbirth_id':get_childbirth_instance.id,
        'childbirth_id':childbirth_id,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/edit_childbirth.html',context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_childbirthView(request,childbirth_id):
    if request.user.is_authenticated and request.user.is_hospital:
        title = request.POST['title']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        dob = request.POST['dob'] 
        gender = request.POST['gender']  
        weight = request.POST['weight']
        race = request.POST['race']
        remark = request.POST['remark'] 
        Childbirth.objects.filter(pk=childbirth_id).update(title=title)
        Childbirth.objects.filter(pk=childbirth_id).update(firstname=firstname)
        Childbirth.objects.filter(pk=childbirth_id).update(lastname=lastname)
        Childbirth.objects.filter(pk=childbirth_id).update(dob=dob)
        Childbirth.objects.filter(pk=childbirth_id).update(gender=gender)
        Childbirth.objects.filter(pk=childbirth_id).update(weight=weight)
        Childbirth.objects.filter(pk=childbirth_id).update(race=race)
        Childbirth.objects.filter(pk=childbirth_id).update(remark=remark)
        messages.info(request,'Update has been done successfully')
        return redirect(f'/edit_childbirth/{childbirth_id}')


@login_required(login_url='/')  
def delete_childbirthView(request, childbirth_id):
    if request.user.is_authenticated and request.user.is_hospital:
        delete_childbirth = Childbirth.objects.get(id=childbirth_id)
        delete_childbirth.delete()
        return redirect('/childbirth_list')
    
       

#===========================================DEATH RECORD========================================
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_deadthrecordView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        title = request.POST['title']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        dod = request.POST['dod'] 
        gender = request.POST['gender']  
        phone = request.POST['phone']
        address = request.POST['address']
        desc = request.POST['desc']
        race = request.POST['race']
        remark = request.POST['remark']
             
        id = random_id(length=9,character_set=string.digits)
    
        save_deadthrecord_details=Deadthrecord(hospital=hospital_instance, id=id, title=title,firstname=firstname, lastname=lastname,
                                            dod=dod, gender=gender,phone=phone, address=address,desc=desc, race=race, remark=remark)
        save_deadthrecord_details.save()
                                             
        messages.info(request,'Death record created successfully')
        return redirect('/add_deadthrecord')
    
       
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_deadthrecordView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        return render(request,'hospital/add_deathrecord.html')
    if request.user.is_authenticated and request.user.is_rep:
        return render(request,'receptionist/add_deathrecord.html')

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def deadthrecord_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        list_all_deadthrecord=Deadthrecord.objects.filter(hospital=hospital_instance)
        deadthrecord_data = {
            'list_all_deadthrecord':list_all_deadthrecord,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/deathrecord_list.html',context=deadthrecord_data)
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        list_all_deadthrecord=Deadthrecord.objects.filter(hospital=hospital_instance)
        deadthrecord_data = {
            'list_all_deadthrecord':list_all_deadthrecord,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'receptionist/deathrecord_list.html',context=deadthrecord_data)
    
@login_required(login_url='/')  
def edit_deathrecordView(request,deathrecord_id):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        get_deathrecord_instance = Deadthrecord.objects.get(id=deathrecord_id)
        data = { 
        'title':get_deathrecord_instance.title,
        'firstname':get_deathrecord_instance.firstname,
        'lastname':get_deathrecord_instance.lastname,
        'dod':get_deathrecord_instance.dod,
        'gender':get_deathrecord_instance.gender,
        'phone':get_deathrecord_instance.phone,
        'address':get_deathrecord_instance.address,
        'desc':get_deathrecord_instance.desc,
        'race':get_deathrecord_instance.race,
        'remark':get_deathrecord_instance.remark,
        'deathrecord_id':get_deathrecord_instance.id,
        'deathrecord_id':deathrecord_id,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/edit_deathrecord.html',context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_deathrecordView(request,deathrecord_id):
    if request.user.is_authenticated and request.user.is_hospital:
        title = request.POST['title']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        dod = request.POST['dod'] 
        gender = request.POST['gender']  
        phone = request.POST['phone']
        address = request.POST['address']
        desc = request.POST['desc']
        race = request.POST['race']
        remark = request.POST['remark']
        Deadthrecord.objects.filter(pk=deathrecord_id).update(title=title)
        Deadthrecord.objects.filter(pk=deathrecord_id).update(firstname=firstname)
        Deadthrecord.objects.filter(pk=deathrecord_id).update(lastname=lastname)
        Deadthrecord.objects.filter(pk=deathrecord_id).update(dod=dod)
        Deadthrecord.objects.filter(pk=deathrecord_id).update(gender=gender)
        Deadthrecord.objects.filter(pk=deathrecord_id).update(phone=phone)
        Deadthrecord.objects.filter(pk=deathrecord_id).update(address=address)
        Deadthrecord.objects.filter(pk=deathrecord_id).update(desc=desc)
        Deadthrecord.objects.filter(pk=deathrecord_id).update(race=race)
        Deadthrecord.objects.filter(pk=deathrecord_id).update(remark=remark)
        messages.info(request,'Update has been done successfully')
        return redirect(f'/edit_deathrecord/{deathrecord_id}')


@login_required(login_url='/')  
def delete_deathrecordView(request, deathrecord_id):
    if request.user.is_authenticated and request.user.is_hospital:
        delete_deathrecord = Deadthrecord.objects.get(id=deathrecord_id)
        delete_deathrecord.delete()
        return redirect('/deadthrecord_list')
    

#===========================================DONOR========================================
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_donorView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        title = request.POST['title']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        bloodgroup = request.POST['bloodgroup'] 
        weight = request.POST['weight']
        age = request.POST['age']
        gender = request.POST['gender']  
        phone = request.POST['phone']
        email = request.POST['email'] 
        quantity = int(request.POST['quantity'] )      
        id = random_id(length=9,character_set=string.digits)
    
        save_donor_details=Donor(hospital=hospital_instance, id=id, title=title, firstname=firstname, lastname=lastname, bloodgroup=bloodgroup, weight=weight, age=age, gender=gender,phone=phone, email=email)
        save_donor_details.save()
        if Blood.objects.filter(hospital=hospital_instance,bloodgroup=bloodgroup).exists():
            existing_blood_group_quantity=int(Blood.objects.values_list('quantity', flat=True).get(bloodgroup=bloodgroup))
            update_blood_quantity=existing_blood_group_quantity + quantity
            Blood.objects.filter(hospital=hospital_instance,bloodgroup=bloodgroup).update(quantity=update_blood_quantity)                             
            messages.info(request,'Blood has been addded successfully to the blood the blood bank')
            return redirect('/add_donor')
        else:
            save_new_blood=Blood(hospital=hospital_instance,bloodgroup=bloodgroup,quantity=quantity)
            save_new_blood.save()
            messages.info(request,'Blood has been addded successfully to the blood the blood bank')
            return redirect('/add_donor')
    else:
        return redirect('/add_donor')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_donorView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/add_donor.html',context=data)
    
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'receptionist/add_donor.html',context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def donor_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        all_donor_list=Donor.objects.filter(hospital=hospital_instance)
        donor_data = {
            'all_donor_list':all_donor_list,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/donor_list.html',context=donor_data)
    
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        all_donor_list=Donor.objects.filter(hospital=hospital_instance)
        donor_data = {
            'all_donor_list':all_donor_list,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
           'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'receptionist/donor_list.html',context=donor_data)
    
@login_required(login_url='/')  
def edit_donorView(request,donorid):
    if request.user.is_authenticated and request.user.is_hospital:
        get_donor_instance = Donor.objects.get(id=donorid)
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
        'title':get_donor_instance.title,
        'firstname':get_donor_instance.firstname,
        'lastname':get_donor_instance.lastname,
        'bloodgroup':get_donor_instance.bloodgroup,
        'weight':get_donor_instance.weight,
        'age':get_donor_instance.age,
        'gender':get_donor_instance.gender,
        'phone':get_donor_instance.phone,
        'email':get_donor_instance.email,
        'donorid':get_donor_instance.id,
        'donorid':donorid,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/edit_donor.html',context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_donorView(request,donorid):
    if request.user.is_authenticated and request.user.is_hospital:
        title = request.POST['title']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        bloodgroup = request.POST['bloodgroup'] 
        weight = request.POST['weight']
        age = request.POST['age']
        gender = request.POST['gender']  
        phone = request.POST['phone']
        email = request.POST['email'] 
        Donor.objects.filter(pk=donorid).update(title=title)
        Donor.objects.filter(pk=donorid).update(firstname=firstname)
        Donor.objects.filter(pk=donorid).update(lastname=lastname)
        Donor.objects.filter(pk=donorid).update(bloodgroup=bloodgroup)
        Donor.objects.filter(pk=donorid).update(weight=weight)
        Donor.objects.filter(pk=donorid).update(age=age)
        Donor.objects.filter(pk=donorid).update(gender=gender)
        Donor.objects.filter(pk=donorid).update(phone=phone)
        Donor.objects.filter(pk=donorid).update(email=email)
        messages.info(request,'Update has been done successfully')
        return redirect(f'/edit_donor/{donorid}')


@login_required(login_url='/')  
def delete_donorView(request, donorid):
    if request.user.is_authenticated and request.user.is_hospital:
        delete_donor = Donor.objects.get(id=donorid)
        delete_donor.delete()
        return redirect('/donor_list')

    
    
#===========================================FILE========================================
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_fileView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        if len(request.FILES) != 0:
            document=request.FILES['document']
            documentfilesize=document.size
            if documentfilesize > 2621440  > 2621440:
                messages.info(request,"The File is Biger Than 2MB")
                return redirect('/add_file')
        title = request.POST['title']
            
        file_id = random_id(length=9,character_set=string.digits)
    
        save_file_details=File(hospital=hospital_instance, id=file_id, title=title, document=document)
        save_file_details.save()
                                             
        messages.info(request,'File created successfully')
        return redirect('/add_file')
    
       
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_fileView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/add_file.html',context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def file_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        all_file_list=File.objects.filter(hospital=hospital_instance)
        file_data = {
            'all_file_list':all_file_list,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/file_list.html',context=file_data)
    
@login_required(login_url='/')  
def edit_fileView(request,file_id):
    if request.user.is_authenticated and request.user.is_hospital:
        get_file_instance = File.objects.get(id=file_id)
        data = {
        'title':get_file_instance.title,
        'document':get_file_instance.document,
        'file_id':get_file_instance.id,
        'file_id':file_id,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/edit_file.html',context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_fileView(request,file_id):
    if request.user.is_authenticated and request.user.is_hospital:
        title = request.POST['title']
        document = request.POST['document']    
        File.objects.filter(pk=file_id).update(title=title)
        File.objects.filter(pk=file_id).update(document=document)
        messages.info(request,'Update has been done successfully')
        return redirect(f'/edit_file/{file_id}')


@login_required(login_url='/')  
def delete_fileView(request, file_id):
    if request.user.is_authenticated and request.user.is_hospital:
        delete_file = File.objects.get(id=file_id)
        delete_file.delete()
        return redirect('/file_list')
    

#===========================================BLOOD========================================
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_bloodView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        bloodgroup = request.POST['bloodgroup']
        quantity = request.POST['quantity']
        status = request.POST['status']       
        id = random_id(length=9,character_set=string.digits)
        save_blood_details=Blood(hospital=hospital_instance, id=id, bloodgroup=bloodgroup, quantity=quantity, status=status)
        save_blood_details.save()
                                             
        messages.info(request,'Blood created successfully')
        return redirect('/add_blood')
    
#===========================================BLOOD FEES========================================
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_blood_feesView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        bloodgroup = request.POST['bloodgroup']
        price = request.POST['price']
        id = random_id(length=9,character_set=string.digits)
        if Bloodfees.objects.filter(hospital=hospital_instance,bloodgroup=bloodgroup).exists():
            messages.info(request,'Blood Group Fees captured already')
            return redirect('/blood_fees')
        else:
            save_blood_group_fees=Bloodfees(hospital=hospital_instance, id=id, bloodgroup=bloodgroup, amount=price)
            save_blood_group_fees.save()           
            messages.info(request,'Blood Fees Save successfully')
            return redirect('/blood_fees')

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def blood_feesView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/blood_fees.html',context=data)

       
@login_required(login_url='/')  
def add_bloodView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/add_blood.html',context=data)
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'receptionist/add_blood.html',context=data)
    
@login_required(login_url='/')  
def income_reportView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/income_report.html',context=data)
    
@login_required(login_url='/')  
def add_assetsView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/add_assets.html',context=data)
    
    
@login_required(login_url='/')  
def create_assetView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        title = request.POST['title']
        amount = int(request.POST['amount'])
        quantity = int(request.POST['quantity'])
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        total = quantity * amount
        create_assets = Assets(hospital=hospital_instance,title=title,amount=amount,quantity=quantity,total=total)
        if create_assets:
            create_assets.save()
            messages.info(request,'Asset save successfully')
            return redirect('/add_assets')
        else:
            return redirect('/add_assets')
        
    
@login_required(login_url='/')  
def income_report_View(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        category = request.POST['category']
        start_date = request.POST['start_date']
        end_date =request.POST['end_date']
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        if category == "Consultation":
            appoint_report =Appointment.objects.filter(hospital=hospital_instance).filter(created_at__gte=start_date, created_at__lt=end_date)[:100]
            if appoint_report:
                data = {
                'appoint_report':appoint_report,
                "hospital_instance":User.objects.get(username=username),
                'total_sum_of_consulation':Appointment.objects.filter(hospital=hospital_instance).aggregate(Sum('amount'))['amount__sum'],
                }
            return render(request,'hospital/income_report.html',context=data) 
        if category == "Blood":
            blood_bank_report =Bloodpurchase.objects.filter(hospital=hospital_instance).filter(created_at__gte=start_date, created_at__lt=end_date)[:100]
            if blood_bank_report:
                data = {
                'blood_bank_report':blood_bank_report,
                "hospital_instance":User.objects.get(username=username),
                'total_sum_of_blood_bank':Bloodpurchase.objects.filter(hospital=hospital_instance).aggregate(Sum('amount'))['amount__sum'],
                }
            return render(request,'hospital/income_report.html',context=data) 
        if category == "Admission":
            admission_report =Admissionfees.objects.filter(hospital=hospital_instance).filter(created_at__gte=start_date, created_at__lt=end_date)[:100]
            if admission_report:
                data = {
                'admission_report':admission_report,
                "hospital_instance":User.objects.get(username=username),
                'total_sum_of_admission_fees':Admissionfees.objects.filter(hospital=hospital_instance).aggregate(Sum('amount'))['amount__sum'],
                }
            return render(request,'hospital/income_report.html',context=data) 
        if category == "Lab":
            laboratory_report =Admissionfees.objects.filter(hospital=hospital_instance).filter(created_at__gte=start_date, created_at__lt=end_date)[:100]
            if laboratory_report:
                data = {
                'laboratory_report':laboratory_report,
                "hospital_instance":User.objects.get(username=username),
                'total_sum_of_laboratory_fees':Labtest.objects.filter(hospital=hospital_instance).aggregate(Sum('amount'))['amount__sum'],
                }
            return render(request,'hospital/income_report.html',context=data) 
        else:
            return redirect('/income_report')

        
@login_required(login_url='/')  
def list_assetsView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        fetch_all_assets = Assets.objects.filter(hospital=hospital_instance).order_by('-created_at')[:50]
        data ={
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        'fetch_all_assets':fetch_all_assets,
        'total_sum_of_assets':Assets.objects.filter(hospital=hospital_instance).aggregate(Sum('total'))['total__sum'],
        'hospital_instance':hospital_instance,
        }
        return render(request,'hospital/asset_list.html',context=data)
    
@login_required(login_url='/')  
def delete_assetsView(request,id):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        fetch_all_assets = Assets.objects.filter(hospital=hospital_instance,id=id).delete()
        if fetch_all_assets:
            # messages.info(request,'Asset Deleted successfully')
            return redirect('/list_assets')
        else:
            return redirect('/add_assets')    
    
@login_required(login_url='/')  
def blood_salesView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        blood_fees =Bloodfees.objects.filter(hospital=hospital_instance)
        data = {
            'hospital_instance':hospital_instance,
            'blood_fees':blood_fees,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
           'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'hospital/blood_sales.html',context=data)
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        blood_fees =Bloodfees.objects.filter(hospital=hospital_instance)
        data ={
            'hospital_instance':hospital_instance,
            'blood_fees':blood_fees,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
           'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'receptionist/blood_sales.html',context=data)
    
@login_required(login_url='/')  
def all_blood_bank_fees_View(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        blood_bank_purchase=Bloodpurchase.objects.filter(hospital=hospital_instance)
        data = {
            'hospital_instance':hospital_instance,
            'blood_bank_purchase':blood_bank_purchase,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
           'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'hospital/blood_bank_purchase.html',context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def blood_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        all_blood_list=Blood.objects.filter(hospital=hospital_instance)
        blood_data = {
            'all_blood_list':all_blood_list,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
           'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'hospital/blood_list.html',context=blood_data)
    
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        all_blood_list=Blood.objects.filter(hospital=hospital_instance)
        blood_data = {
            'all_blood_list':all_blood_list,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
           'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'receptionist/blood_list.html',context=blood_data)
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def blood_list_feesView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        all_blood_list_fees=Bloodfees.objects.filter(hospital=hospital_instance)
        blood_data = {
            'all_blood_list_fees':all_blood_list_fees,
            'hospital_instance':hospital_instance,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
           'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'hospital/blood_list_fees.html',context=blood_data)
    
    
@login_required(login_url='/')  
def edit_bloodView(request,blood_id):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        get_blood_instance = Blood.objects.get(id=blood_id)
        data = { 
        'bloodgroup':get_blood_instance.bloodgroup,
        'quantity':get_blood_instance.quantity,
        'status':get_blood_instance.status,
        'blood_id':get_blood_instance.id,
        'blood_id':blood_id,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0), 
        }
        return render(request,'hospital/edit_blood.html',context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_bloodView(request,blood_id):
    if request.user.is_authenticated and request.user.is_hospital:
        bloodgroup = request.POST['bloodgroup']
        quantity = request.POST['quantity']
        status = request.POST['status']  
        Blood.objects.filter(pk=blood_id).update(bloodgroup=bloodgroup)
        Blood.objects.filter(pk=blood_id).update(quantity=quantity)
        Blood.objects.filter(pk=blood_id).update(status=status)
        messages.info(request,'Update has been done successfully')
        return redirect(f'/edit_blood/{blood_id}')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_blood_salesView(request):
    if request.user.is_authenticated and request.user.is_hospital  and request.method=="POST":
        patientid = request.POST['patientid']
        bloodgroup = request.POST['bloodgroup']
        quantity = request.POST['quantity']
        paymenttype = request.POST['paymenttype']  
        
        if not Patient.objects.filter(phone=patientid).exists():
            messages.info(request,'Patient ID not found in the system')
            return redirect('/blood_sales')
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        patient_instance=Patient.objects.get(phone=patientid)
        blood_group_price=int(Bloodfees.objects.filter(bloodgroup=bloodgroup).values_list('amount', flat=True).get(hospital=hospital_instance))
        avaliable_quantity_bank=int(Blood.objects.filter(bloodgroup=bloodgroup).values_list('quantity', flat=True).get(hospital=hospital_instance))
        total_purchase_price=blood_group_price * int(quantity)
        
        if int(quantity) > avaliable_quantity_bank:
            messages.info(request,'The requsted quantity is more than the avaliable quantity')
            return redirect('/blood_sales')
        else:
            save_blood_fees=Bloodpurchase(hospital=hospital_instance, patient=patient_instance, bloodgroup=bloodgroup, quantity=quantity, amount=total_purchase_price,status=paymenttype)
            save_blood_fees.save()
            new_avaliabe_quantity = avaliable_quantity_bank - int(quantity)
            Blood.objects.filter(hospital=hospital_instance,bloodgroup=bloodgroup).update(quantity=new_avaliabe_quantity)
            messages.info(request,'Blood has been successfully purchase')
            return redirect('/blood_sales')
    if request.user.is_authenticated and request.user.is_rep  and request.method=="POST":
        patientid = request.POST['patientid']
        bloodgroup = request.POST['bloodgroup']
        quantity = request.POST['quantity']
        paymenttype = request.POST['paymenttype']  
        
        if not Patient.objects.filter(phone=patientid).exists():
            messages.info(request,'Patient ID not found in the system')
            return redirect('/blood_sales')
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        patient_instance=Patient.objects.get(phone=patientid)
        blood_group_price=int(Bloodfees.objects.filter(bloodgroup=bloodgroup).values_list('amount', flat=True).get(hospital=hospital_instance))
        avaliable_quantity_bank=int(Blood.objects.filter(bloodgroup=bloodgroup).values_list('quantity', flat=True).get(hospital=hospital_instance))
        total_purchase_price=blood_group_price * int(quantity)
        
        if int(quantity) > avaliable_quantity_bank:
            messages.info(request,'The requsted quantity is more than the avaliable quantity')
            return redirect('/blood_sales')
        else:
            save_blood_fees=Bloodpurchase(hospital=hospital_instance, patient=patient_instance, bloodgroup=bloodgroup, quantity=quantity, amount=total_purchase_price,status=paymenttype)
            save_blood_fees.save()
            new_avaliabe_quantity = avaliable_quantity_bank - int(quantity)
            Blood.objects.filter(hospital=hospital_instance,bloodgroup=bloodgroup).update(quantity=new_avaliabe_quantity)
            messages.info(request,'Blood has been successfully purchase')
            return redirect('/blood_sales')

@login_required(login_url='/')  
def delete_bloodView(request, blood_id):
    if request.user.is_authenticated and request.user.is_hospital:
        delete_blood=Blood.objects.get(id=blood_id)
        delete_blood.delete()
        return redirect('/blood_list')
    
@login_required(login_url='/')  
def delete_blood_feesView(request,id):
    if request.user.is_authenticated and request.user.is_hospital:
        delete_blood=Bloodfees.objects.get(id=id)
        delete_blood.delete()
        return redirect('/blood_list_fees')

#===========================================NOTICES========================================
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_noticeView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        title = request.POST['title']
        noticfor = request.POST['noticfor']
        noticemsg = request.POST['noticemsg']
        status = request.POST['status']       
        notice_id = random_id(length=9,character_set=string.digits)
        noticfor_instance = Department.objects.get(id=noticfor)
        save_notice_details=Notices(hospital=hospital_instance, id=notice_id, noticfor=noticfor_instance, title=title, noticemsg=noticemsg, status=status)
        save_notice_details.save()
                                             
        messages.info(request,'Notice created successfully')
        return redirect('/add_notice')
    
    
       
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_noticeView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        get_all_hospital_department_list = Department.objects.filter(hospital=hospital_instance)
        data = {
            'get_all_hospital_department_list':get_all_hospital_department_list,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/add_notice.html',context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def notice_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        all_notice_list=Notices.objects.filter(hospital=hospital_instance)
        notice_data = {
            'all_notice_list':all_notice_list,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/notice_list.html',context=notice_data )
    


@login_required(login_url='/')  
def edit_noticeView(request,notice_id):
    if request.user.is_authenticated and request.user.is_hospital:
        get_notice_instance = Notices.objects.get(id=notice_id),
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
        'title':get_notice_instance.title,
        'noticfor':get_notice_instance.noticfor,
        'noticemsg':get_notice_instance.noticemsg,
        'status':get_notice_instance.status,
        'notice_id':get_notice_instance.id,
        'notice_id':notice_id,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/edit_notice.html',context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_noticeView(request,notice_id):
    if request.user.is_authenticated and request.user.is_hospital:
        title = request.POST['title']
        noticfor = request.POST['noticfor']
        noticemsg = request.POST['noticemsg']
        status = request.POST['status']     
        Notices.objects.filter(pk=notice_id).update(title=title)
        Notices.objects.filter(pk=notice_id).update(noticfor=noticfor)
        Notices.objects.filter(pk=notice_id).update(noticemsg=noticemsg)
        Notices.objects.filter(pk=notice_id).update(status=status)
        messages.info(request,'Update has been done successfully')
        return redirect(f'/edit_notice/{notice_id}')


@login_required(login_url='/')  
def delete_noticeView(request, notice_id):
    if request.user.is_authenticated and request.user.is_hospital:
        delete_notice = Notices.objects.get(id=notice_id)
        delete_notice.delete()
        return redirect('/notice_list')


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def doctors_profileView(request,doctor_id):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        doctors_instance = Doctor.objects.get(id=doctor_id)
        data = {
        'doctorsnames':doctors_instance.name,
        'department':doctors_instance.department.name,
        'departmentdec':doctors_instance.department.desc,
        'phone':doctors_instance.phone,
        'address':doctors_instance.address,
        'email':doctors_instance.email,
        'departmentid':doctors_instance.departmentid,
        'picture':doctors_instance.picture,
        'message_about_dr':doctors_instance.message_about_dr,
        'doctorsappointment':Appointment.objects.filter(hospital=hospital_instance,status=0).filter(dr=doctors_instance),
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/doctorsprofile.html',context=data)
    
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        doctors_instance = Doctor.objects.get(id=doctor_id)
        data = {
        'doctorsnames':doctors_instance.name,
        'department':doctors_instance.department.name,
        'departmentdec':doctors_instance.department.desc,
        'phone':doctors_instance.phone,
        'address':doctors_instance.address,
        'email':doctors_instance.email,
        'departmentid':doctors_instance.departmentid,
        'picture':doctors_instance.picture,
        'message_about_dr':doctors_instance.message_about_dr,
        'doctorsappointment':Appointment.objects.filter(hospital=hospital_instance,status=0).filter(dr=doctors_instance),
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'receptionist/doctorsprofile.html',context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def patient_detailsView(request,patient_id):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        patient_instance=Patient.objects.get(id=patient_id)
        patient_history=Phistory.objects.filter(patient=patient_instance)
        data = {
        'patient_id':patient_instance.id,
        'title':patient_instance.title,
        'name':patient_instance.name,
        'nok':patient_instance.nok,
        'non':patient_instance.non,
        'phone':patient_instance.phone,
        'created_at':patient_instance.created_at,
        'patient_appointment':Appointment.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(status=1)[:1],
        'patient_treatment_log':Treatment.objects.filter(hospital=hospital_instance,patient=patient_instance)[:5],
        'patient_history':patient_history,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/patient_details.html',context=data)
    
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        patient_instance=Patient.objects.get(id=patient_id)
        patient_history=Phistory.objects.filter(patient=patient_instance)
        data = {
        'patient_id':patient_instance.id,
        'title':patient_instance.title,
        'name':patient_instance.name,
        'nok':patient_instance.nok,
        'non':patient_instance.non,
        'phone':patient_instance.phone,
        'created_at':patient_instance.created_at,
        'patient_appointment':Appointment.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(status=1)[:1],
        'patient_treatment_log':Treatment.objects.filter(hospital=hospital_instance,patient=patient_instance)[:5],
        'patient_history':patient_history,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'receptionist/patient_details.html',context=data)
    
    if request.user.is_authenticated and request.user.is_dr:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=doctor_instance.hospital.username)
        patient_instance=Patient.objects.get(id=patient_id)
        patient_history=Phistory.objects.filter(patient=patient_instance)
        data = {
        'patient_id':patient_instance.id,
        'title':patient_instance.title,
        'name':patient_instance.name,
        'nok':patient_instance.nok,
        'non':patient_instance.non,
        'phone':patient_instance.phone,
        'patient_instance':patient_instance,
        'created_at':patient_instance.created_at,
        'patient_appointment':Appointment.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(status=1)[:1],
        'patient_treatment_log':Treatment.objects.filter(hospital=hospital_instance,patient=patient_instance)[:5],
        'patient_history':patient_history,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'doctor/patient_details.html',context=data)
    
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def search_patient_detailView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.POST['cellphone']:
        cell_phone = request.POST['cellphone']
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        if not Patient.objects.filter(phone=cell_phone,hospital=hospital_instance).exists():
            return redirect('/hospital_dashboard')
        else:
            patient_instance=Patient.objects.get(phone=cell_phone)
            data = {
            'patient_id':patient_instance.id,
            'title':patient_instance.title,
            'name':patient_instance.name,
            'nok':patient_instance.nok,
            'non':patient_instance.non,
            'phone':patient_instance.phone,
            'patient_history':Phistory.objects.filter(patient=patient_instance),
            'created_at':patient_instance.created_at,
            'patient_appointment':Appointment.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(status=1)[:1],
            'patient_treatment_log':Treatment.objects.filter(hospital=hospital_instance,patient=patient_instance)[:5],
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
            }
            return render(request,'hospital/patient_details.html',context=data)
    
    if request.user.is_authenticated and request.user.is_rep and request.POST['cellphone']:
        cell_phone = request.POST['cellphone']
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        if not Patient.objects.filter(phone=cell_phone,hospital=hospital_instance).exists():
            return redirect('/recepdashboard')
        else:
            patient_instance=Patient.objects.get(phone=cell_phone)
            data = {
            'patient_id':patient_instance.id,
            'title':patient_instance.title,
            'name':patient_instance.name,
            'nok':patient_instance.nok,
            'non':patient_instance.non,
            'phone':patient_instance.phone,
            'patient_history':Phistory.objects.filter(patient=patient_instance),
            'created_at':patient_instance.created_at,
            'patient_appointment':Appointment.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(status=1)[:1],
            'patient_treatment_log':Treatment.objects.filter(hospital=hospital_instance,patient=patient_instance)[:5],
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
            }
            return render(request,'receptionist/patient_details.html',context=data)
    if request.user.is_authenticated and request.user.is_dr and request.POST['cellphone']:
        cell_phone = request.POST['cellphone']
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=doctor_instance.hospital.username)
        if not Patient.objects.filter(phone=cell_phone,hospital=hospital_instance).exists():
            return redirect('/recepdashboard')
        else:
            patient_instance=Patient.objects.get(phone=cell_phone)
            data = {
            'patient_id':patient_instance.id,
            'title':patient_instance.title,
            'name':patient_instance.name,
            'nok':patient_instance.nok,
            'non':patient_instance.non,
            'patient_history':Phistory.objects.filter(patient=patient_instance),
            'phone':patient_instance.phone,
            'created_at':patient_instance.created_at,
            'patient_appointment':Appointment.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(status=1)[:1],
            'patient_treatment_log':Treatment.objects.filter(hospital=hospital_instance,patient=patient_instance)[:5],
            'doctor_instance_to_display_profile_picture':doctor_instance,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
            }
            return render(request,'doctor/patient_details.html',context=data)
        
@login_required(login_url='/')  
def doctorsdashboardView(request):
    if request.user.is_authenticated and request.user.is_dr:
        todays_date = date.today()
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=customer_instance)
        data={
            'doctors_appointment':Appointment.objects.filter(dr=doctor_instance,astatus=0),
            'doctors_appoint_count':Appointment.objects.filter(dr=doctor_instance).count(),
            'pend_treatment_count':Treatment.objects.filter(dr=doctor_instance,tstatus=0).count(),
            'com_treatment_count':Treatment.objects.filter(dr=doctor_instance,tstatus=1).count(),
            'todaysappointment':Appointment.objects.filter(dr=doctor_instance,date=todays_date).count(),
            'completed_treatment_log':Treatment.objects.filter(dr=doctor_instance,tstatus=1),
            'doctor_instance_to_display_profile_picture':doctor_instance,
        }
        return render(request,'doctor/index.html',context=data) 
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def labdashboardView(request):
    if request.user.is_authenticated and request.user.is_lab:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=doctor_instance.hospital.username)
        data={
            'labtest_count':Lapreport.objects.filter(hospital=hospital_instance).count(),
            'completed_report_count':Treatment.objects.filter(hospital=hospital_instance,tstatus=1).count(),
            'pending_report_count':Treatment.objects.filter(hospital=hospital_instance,tstatus=0).count(),
            'completed_treatment_log':Treatment.objects.filter(hospital=hospital_instance,tstatus=1),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'laboratory/index.html',context=data) 
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def recepdashboardView(request):
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        data = {
        'count_number_of_patient':Patient.objects.filter(hospital=hospital_instance).count(),
        'count_number_of_doctors':Doctor.objects.filter(hospital=hospital_instance).count(),
        'count_number_of_appointment':Appointment.objects.filter(hospital=hospital_instance,status=0).count(),
        'count_number_of_treatment':Treatment.objects.filter(hospital=hospital_instance,tstatus__gt=0).count(),
        'doctor_list':Doctor.objects.filter(hospital=hospital_instance),
        'patient_list':Patient.objects.filter(hospital=hospital_instance)[:10],
        'reception_instance_to_display_profile_picture':recep_instance,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'receptionist/index.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def phamardashboardView(request):
    if request.user.is_authenticated and request.user.is_pha:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=doctor_instance.hospital.username)
        data={
            'labtest_count':Lapreport.objects.filter(hospital=hospital_instance).count(),
            'completed_report_count':Treatment.objects.filter(hospital=hospital_instance,tstatus=1).count(),
            'pending_report_count':Treatment.objects.filter(hospital=hospital_instance,tstatus=0).count(),
            'completed_treatment_log':Treatment.objects.filter(hospital=hospital_instance,tstatus=1),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'phamarcy/index.html',context=data) 
    else:
        return redirect('/')
  
from django.db.models import Q
@login_required(login_url='/')  
def doctortreatmentView(request,patientid,apoint_id):
    if request.user.is_authenticated and request.user.is_dr:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=doctor_instance.hospital.username)
        patient_instance=Patient.objects.get(phone=patientid)
        data={
            'doctors_appointment':Appointment.objects.filter(dr=doctor_instance,status=0).filter(id=patientid),
            'payment_categories':Paymentcategory.objects.filter(hospital=hospital_instance),
            'Patienttest':Patienttest.objects.filter(patient=patient_instance,hospital=hospital_instance).filter(Q(status=0) | Q(status=2)),
            'patient_lab_report':Labresult.objects.filter(patient=patient_instance,hospital=hospital_instance).filter(status=1),
            'patientid':patientid,
            'treatmentlog':Treatment.objects.filter(patient=patient_instance,hospital=hospital_instance).filter(dr=doctor_instance,tstatus=0).count(),
            'lab_report_status':Treatment.objects.filter(patient=patient_instance,hospital=hospital_instance).filter(dr=doctor_instance,tstatus=1).count(),
            'apoint_id':apoint_id,
            'doctor_instance_to_display_profile_picture':doctor_instance,
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'doctor/treatment.html',context=data) 
    else:
        return redirect('/')
    

@transaction.atomic  #transactional  
@login_required(login_url='/')  
def add_patient_testView(request,patientid,apoint_id):
    if request.user.is_authenticated and request.user.is_dr and request.method=="POST":
        categoryname = request.POST['categoryname']
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=doctor_instance.hospital.username)
        patient_instance=Patient.objects.get(phone=patientid)
        category_amount=Paymentcategory.objects.values_list('amount', flat=True).get(category=categoryname)
        unique_test_id=random_id(length=8,character_set=string.digits)
        
        if Patienttest.objects.filter(category=categoryname,patient=patient_instance).filter(status=0).exists():
            return redirect(f'/doctortreatment/{patientid}/{apoint_id}') 
        
        if Patienttest.objects.filter(hospital=hospital_instance,status=0).filter(patient=patient_instance).count() > 0:
            existing_test_id=Patienttest.objects.filter(patient=patient_instance,status=0).values_list('testid', flat=True)
            add_test=Patienttest(hospital=hospital_instance,category=categoryname,amount=category_amount,patient=patient_instance,testid=existing_test_id)
            add_test.save()
            Treatment.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(treatmentid=0).update(treatmentid=existing_test_id)
            return redirect(f'/doctortreatment/{patientid}/{apoint_id}') 
        else:
            add_test=Patienttest(hospital=hospital_instance,category=categoryname,amount=category_amount,patient=patient_instance,testid=unique_test_id)
            add_test.save()
            Treatment.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(treatmentid=0).update(treatmentid=unique_test_id)
            return redirect(f'/doctortreatment/{patientid}/{apoint_id}')
    else:
        return redirect('/')
    
    
@transaction.atomic  #transactional  
@login_required(login_url='/')  
def delete_patient_testView(request,patientid,test_id,apoint_id):
    if request.user.is_authenticated and request.user.is_dr:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=doctor_instance.hospital.username)
        Patienttest.objects.filter(hospital=hospital_instance,id=test_id).delete()
        return redirect(f'/doctortreatment/{patientid}/{apoint_id}') 
    else:
        return redirect('/')
    

@transaction.atomic  #transactional  
@login_required(login_url='/')  
def create_treatmentView(request,patientid,apoint_id):
    if request.user.is_authenticated and request.user.is_dr and request.method=="POST":
        patient_status = request.POST['status']
        desc = request.POST['desc']
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=doctor_instance.hospital.username)
        patient_instance=Patient.objects.get(phone=patientid)
        unique_test_id=random_id(length=8,character_set=string.digits)
        
        if Patienttest.objects.filter(hospital=hospital_instance,status=0).filter(patient=patient_instance).count() > 0:
            existing_test_id=Patienttest.objects.filter(hospital=hospital_instance,status=0).filter(patient=patient_instance).latest('testid')
            create_patient_treatment=Treatment(hospital=hospital_instance,patient=patient_instance,dr=doctor_instance,desc=desc,pstate=patient_status,treatmentid=existing_test_id)
            if create_patient_treatment:
                create_patient_treatment.save()
                Appointment.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(dr=doctor_instance).update(status=1)
                Patienttest.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(status=0).update(status=1)
                # messages.success(request,'Patient has been consulted successfuly.')
                return redirect(f'/doctortreatment/{patientid}/{apoint_id}') 
        else:
            create_patient_treatment=Treatment(hospital=hospital_instance,patient=patient_instance,dr=doctor_instance,desc=desc,pstate=patient_status,treatmentid=unique_test_id)
            if create_patient_treatment:
                create_patient_treatment.save()
                Appointment.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(dr=doctor_instance).update(status=1)
                Patienttest.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(status=0).update(status=1)
                # messages.success(request,'Patient has been consulted successfuly.')
                return redirect(f'/doctortreatment/{patientid}/{apoint_id}') 
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def treatment_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data={
            'pending_treatment_log':Treatment.objects.filter(hospital=hospital_instance,tstatus=0),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/treatment_list.html',context=data) 
    
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=doctor_instance.hospital.username)
        data={
            'pending_treatment_log':Treatment.objects.filter(hospital=hospital_instance,tstatus=0),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'receptionist/treatment_list.html',context=data) 
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def completed_treatment_listView(request):
    if request.user.is_authenticated and request.user.is_lab:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=doctor_instance.hospital.username)
        data={
            'completed_treatment_log':Labresult.objects.filter(hospital=hospital_instance,status=1),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'laboratory/completed_treatment_list.html',context=data) 
    
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        user_instance=User.objects.get(username=username)
        hospital_instance=User.objects.get(username=user_instance)
        data={
            'completed_treatment_log':Labresult.objects.filter(hospital=hospital_instance,status=0),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/completed_treatment_list.html',context=data) 
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username) 
        data={
            'completed_treatment_log':Labresult.objects.filter(hospital=hospital_instance,status=0),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'receptionist/completed_treatment_list.html',context=data) 
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def print_patient_reportView(request,patientid,treatid):
    if request.user.is_authenticated and request.user.is_rep:
        patient_instance=Patient.objects.get(phone=patientid)
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=doctor_instance.hospital.username)
        data={
            'patient_treatment_report':Treatment.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(id=treatid),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'receptionist/doctors_report.html',context=data) 
    
    if request.user.is_authenticated and request.user.is_dr:
        patient_instance=Patient.objects.get(phone=patientid)
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=doctor_instance.hospital.username)
        data={
            'patient_treatment_report':Treatment.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(id=treatid),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'doctor/doctors_report.html',context=data) 
    else:
        return redirect('/')

    
@login_required(login_url='/')  
def labtestView(request):
    if request.user.is_authenticated and request.user.is_lab:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=doctor_instance.hospital.username)
        data={
            'labtest':Lapreport.objects.filter(hospital=hospital_instance,status="Processing"),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'laboratory/labtest.html',context=data) 
    
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        user_instance=User.objects.get(username=username)
        hospital_instance=User.objects.get(username=user_instance)
        data={
            'labtest':Lapreport.objects.filter(hospital=hospital_instance,status="Processing"),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'hospital/labtest.html',context=data) 
    
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username) 
        data={
            'labtest':Lapreport.objects.filter(hospital=hospital_instance,status="Processing"),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'receptionist/labtest.html',context=data) 
    else:
        return redirect('/')
    

@login_required(login_url='/')  
def record_reportView(request,patient_id):
    if request.user.is_authenticated and request.user.is_lab:
        username=request.user.username
        user_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=user_instance)
        hospital_user_name=doctor_instance.hospital.username
        hospital_instance=User.objects.get(username=hospital_user_name)
        patient_instance=Patient.objects.get(phone=patient_id)
        data={
            'patient_test_list':Patienttest.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(status=1),
            'patientid':patient_id,
            'patient_lab_report':Labresult.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(status=0),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0),
        }
        return render(request,'laboratory/record_report.html',context=data) 
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def record_resultView(request,patient_id):
    if request.user.is_authenticated and request.user.is_lab and request.method=="POST":
        testname=request.POST['testname']
        result=request.POST['result']
        username=request.user.username
        user_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=user_instance)
        hospital_user_name=doctor_instance.hospital.username
        hospital_instance=User.objects.get(username=hospital_user_name)
        patient_instance=Patient.objects.get(phone=patient_id)
        if Labresult.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(testname=testname,testreport=result).exists():
            messages.success(request,'Result has been captured already.')
            return redirect(f'/record_report/{patient_id}')
        else:
            patient_test_id=Patienttest.objects.filter(patient=patient_instance,status=1).values_list('testid', flat=True)
            create_result=Labresult(hospital=hospital_instance,patient=patient_instance,testname=testname,testreport=result,testid=patient_test_id)
            create_result.save()
            return redirect(f'/record_report/{patient_id}')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def delete_resultView(request,patient_id,result_id):
    if request.user.is_authenticated and request.user.is_lab:
        username=request.user.username
        user_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=user_instance)
        hospital_user_name=doctor_instance.hospital.username
        hospital_instance=User.objects.get(username=hospital_user_name)
        patient_instance=Patient.objects.get(phone=patient_id)
        if Labresult.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(id=result_id).delete():
            return redirect(f'/record_report/{patient_id}')
    else:
        return redirect('/')
    

@login_required(login_url='/')  
@transaction.atomic  #transactional  
def record_report_statusView(request,patient_id):
    if request.user.is_authenticated and request.user.is_lab and request.method=="POST":
        labstatus=request.POST['labstatus']
        username=request.user.username
        user_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=user_instance)
        hospital_user_name=doctor_instance.hospital.username
        hospital_instance=User.objects.get(username=hospital_user_name)
        patient_instance=Patient.objects.get(phone=patient_id)
        Lapreport.objects.filter(hospital=hospital_instance,patient=patient_instance).update(status=labstatus)
        Treatment.objects.filter(hospital=hospital_instance,patient=patient_instance).update(tstatus=1)
        Patienttest.objects.filter(hospital=hospital_instance,patient=patient_instance).update(status=2)
        Labresult.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(status=0).update(status=1)
        return redirect(f'/completed_treatment_list')
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
@transaction.atomic  #transactional  
def prescribe_treatmentView(request,patient_id,apoint_id):
    if request.user.is_authenticated and request.user.is_dr and request.method=="POST":
        patient_status=request.POST['patient_status']
        dname=request.POST['dname']
        prescription=request.POST['prescription']
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        patient_instance=Patient.objects.get(phone=patient_id)
        Appointment.objects.filter(id=apoint_id).update(astatus=1)
        create_patient_treatment=Treatment.objects.get(patient=patient_instance)
        create_patient_treatment.remark=prescription
        create_patient_treatment.dname=dname
        create_patient_treatment.pstate=patient_status
        create_patient_treatment.save()
        return redirect(f'/doctorsdashboard')
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def my_doctors_appointmentView(request):
    if request.user.is_authenticated and request.user.is_dr: 
        todays_date = date.today()
        username=request.user.username
        user_instance = User.objects.get(username=username)
        dr_instance=Doctor.objects.get(user=user_instance) 
        data = {
        'my_appointment_list':Appointment.objects.filter(dr=dr_instance,date=todays_date).filter(astatus=0),
        'my_upcoming_appointment_list':Appointment.objects.filter(dr=dr_instance,astatus=0),
        'app_message_count':Messages.objects.filter(hospital=user_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=user_instance,status=0),
        }       
        return render(request,'doctor/appointment_list.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def my_doctors_com_appointmentView(request):
    if request.user.is_authenticated and request.user.is_dr: 
        todays_date = date.today()
        username=request.user.username
        user_instance = User.objects.get(username=username)
        dr_instance=Doctor.objects.get(user=user_instance) 
        data = {
        'my_completed_appointment_list':Appointment.objects.filter(dr=dr_instance,astatus=1),
        'app_message_count':Messages.objects.filter(hospital=user_instance,status=0).count(),
        'app_message':Messages.objects.filter(hospital=user_instance,status=0),
        }       
        return render(request,'doctor/appointment_list.html',context=data)
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def my_doctors_com_treatmentView(request):
    if request.user.is_authenticated and request.user.is_dr:
        username=request.user.username
        user_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=user_instance)
        hospital_user_name=doctor_instance.hospital.username
        hospital_instance=User.objects.get(username=hospital_user_name)
        data={
           'completed_treatment_log':Treatment.objects.filter(dr=doctor_instance,tstatus=1).filter(hospital=hospital_instance),
            'app_message_count':Messages.objects.filter(hospital=user_instance,status=0).count(),
           'app_message':Messages.objects.filter(hospital=user_instance,status=0),
        }
        return render(request,'doctor/completed_treatment_list.html',context=data) 

    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        user_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=user_instance)
        hospital_user_name=doctor_instance.hospital.username
        hospital_instance=User.objects.get(username=hospital_user_name)
        data={
           'completed_treatment_log':Treatment.objects.filter(tstatus=1,hospital=hospital_instance),
            'app_message_count':Messages.objects.filter(hospital=user_instance,status=0).count(),
           'app_message':Messages.objects.filter(hospital=user_instance,status=0),
        }
        return render(request,'receptionist/completed_treatment_list.html',context=data) 
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def my_doctors_pend_treatmentView(request):
    if request.user.is_authenticated and request.user.is_dr:
        username=request.user.username
        user_instance = User.objects.get(username=username)
        dr_instance=Doctor.objects.get(user=user_instance) 
        data={
            'pending_treatment_log':Treatment.objects.filter(dr=dr_instance,tstatus=0),
            'app_message_count':Messages.objects.filter(hospital=user_instance,status=0).count(),
            'app_message':Messages.objects.filter(hospital=user_instance,status=0),
        }
        return render(request,'doctor/treatment_list.html',context=data) 
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def lab_reportView(request,patient_id,testid):
    if request.user.is_authenticated and request.user.is_lab:
        username=request.user.username
        user_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=user_instance)
        hospital_user_name=doctor_instance.hospital.username
        hospital_instance=User.objects.get(username=hospital_user_name)   
        patient_instance=Patient.objects.get(phone=patient_id)
          
        data = {
           'hospital_instance':hospital_instance,
           'doctor_instance':doctor_instance,
           'patient_instance':patient_instance,
           'patient_com_test_list':Labresult.objects.filter(testid=testid),
           'todaysdate':date.today(),
            'app_message_count':Messages.objects.filter(hospital=user_instance,status=0).count(),
           'app_message':Messages.objects.filter(hospital=user_instance,status=0),
        }
        return render(request,'laboratory/lab_report.html',context=data) 
    else:
        return redirect('/')
    

@login_required(login_url='/')  
def active_hospital_listView(request):
    if request.user.is_authenticated and request.user.is_superuser: 
        data = {
        'active_hospital_list':User.objects.filter(is_hospital=True,is_activation=True),
        }       
        return render(request,'superadmin/hospital_list.html',context=data)
    else:
        return redirect('/')
    

@login_required(login_url='/')  
def inactive_hospital_listView(request):
    if request.user.is_authenticated and request.user.is_superuser: 
        data = {
        'inactive_hospital_list':User.objects.filter(is_hospital=True,is_activation=False),
        }       
        return render(request,'superadmin/hospital_list.html',context=data)
    else:
        return redirect('/')
    

@login_required(login_url='/')  
def suspend_hospitalView(request,hospital_id):
    if request.user.is_authenticated and request.user.is_superuser:  
        User.objects.filter(id=hospital_id).update(is_activation=False)    
        return redirect('/active_hospital_list')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def unsuspend_hospitalView(request,hospital_id):
    if request.user.is_authenticated and request.user.is_superuser:  
        User.objects.filter(id=hospital_id).update(is_activation=True)    
        return redirect('/inactive_hospital_list')
    else:
        return redirect('/')
    


@login_required(login_url='/')  
def paid_hospital_listView(request):
    if request.user.is_authenticated and request.user.is_superuser: 
        data = {
        'paid_hospital_list':Fees.objects.filter(status=1)
        }       
        return render(request,'superadmin/payment_list.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def unpaid_hospital_listView(request):
    if request.user.is_authenticated and request.user.is_superuser: 
        data = {
        'unpaid_hospital_list':User.objects.filter(is_hospital=True,is_activation=True).filter(is_paid=False),
        }       
        return render(request,'superadmin/payment_list.html',context=data)
    else:
        return redirect('/')
    

@login_required(login_url='/')  
def superadmin_paymentView(request,hospital_id):
    if request.user.is_authenticated and request.user.is_superuser:
        data={
        'hospital_id':hospital_id
        }      
        return render(request,'superadmin/payment.html',context=data)
    else:
        return redirect('/')

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def processsuperadmin_paymentView(request,hospital_id):
    if request.user.is_authenticated and request.user.is_superuser and request.method=="POST":
        pakage=request.POST['pakage']
        amount=request.POST['amount']
        if pakage == "Monthly":
            hospital_instance=User.objects.get(id=hospital_id)
            from datetime import datetime, timedelta
            dt = datetime.now()
            td = timedelta(days=28)
            my_date = dt + td
            pakageregisterdate=date.today()
            pakageexpiredate = my_date.date()
            record_licence_fees=Fees(hospital=hospital_instance,pakage=pakage,amount=amount,paiddate=pakageregisterdate,expireddate=pakageexpiredate)
            record_licence_fees.save()
            hospital_instance.is_paid=True
            hospital_instance.save()  
            Fees.objects.filter(hospital=hospital_instance,status=0).update(status=1)          
            messages.info(request,'Software Licence has been paid successfully')
            return redirect('/paid_hospital_list')
        if pakage == "Yearly":
            hospital_instance=User.objects.get(id=hospital_id)
            from datetime import datetime, timedelta
            dt = datetime.now()
            td = timedelta(days=365)
            my_date = dt + td
            pakageregisterdate=date.today()
            pakageexpiredate = my_date.date()
            record_licence_fees=Fees(hospital=hospital_instance,pakage=pakage,amount=amount,paiddate=pakageregisterdate,expireddate=pakageexpiredate)
            record_licence_fees.save()
            hospital_instance.is_paid=True
            hospital_instance.save()
            Fees.objects.filter(hospital=hospital_instance,status=0).update(status=1)
            messages.info(request,'Software Licence has been paid successfully')
            return redirect('/paid_hospital_list')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def app_notification_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
            'app_notification_messages':Messages.objects.filter(hospital=hospital_instance).order_by('-created_at'),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=9).order_by('-created_at'),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),

        }      
        return render(request,'hospital/app_message_list.html',context=data)

    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=doctor_instance.hospital.username)
        data = {
            'app_notification_messages':Messages.objects.filter(hospital=hospital_instance).order_by('-created_at'),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance).count(),
            'app_message':Messages.objects.filter(hospital=hospital_instance,status=0).order_by('-created_at'),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        }      
        return render(request,'receptionist/app_message_list.html',context=data)
    
    
@login_required(login_url='/')  
def app_notification_detailView(request,messageid):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        Messages.objects.filter(id=messageid).update(status=1)
        data = {
            'app_notification_message_detail':Messages.objects.get(id=messageid),
            'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        }      
        return render(request,'hospital/app_message_list.html',context=data)

    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
        'app_notification_message_detail':Messages.objects.get(id=messageid),
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        }       
        return render(request,'receptionist/app_message_list.html',context=data)
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def appointment_reportView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        }         
        return render(request,'hospital/appointment_report.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def monthly_expenses_reportView(request):
    if request.user.is_authenticated and request.user.is_hospital:  
        username=request.user.username
        hospital_instance=User.objects.get(username=username) 
        data = {
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        }     
        return render(request,'hospital/monthly_report.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def laboratory_reportView(request):
    if request.user.is_authenticated and request.user.is_hospital: 
        username=request.user.username
        hospital_instance=User.objects.get(username=username) 
        data = {
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        }        
        return render(request,'hospital/laboratory_report.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def admission_reportView(request):
    if request.user.is_authenticated and request.user.is_hospital: 
        username=request.user.username
        hospital_instance=User.objects.get(username=username) 
        data = {
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        }        
        return render(request,'hospital/admission_report.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def blood_bank_reportView(request):
    if request.user.is_authenticated and request.user.is_hospital: 
        username=request.user.username
        hospital_instance=User.objects.get(username=username) 
        data = {
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        }        
        return render(request,'hospital/blood_bank_report.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def generate_appointment_reportView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST" and request.POST['from_date'] and request.POST['to_date']:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        from_date = request.POST['from_date'] 
        to_date = request.POST['to_date']  
        selected_appointment_report=Appointment.objects.filter(hospital=hospital_instance,created_at__range=(from_date,to_date))
        current_date = datetime.date.today()
        data ={
        'selected_appointment_report':selected_appointment_report,
        'total_appointment_cash':Appointment.objects.filter(hospital=hospital_instance,created_at__range=(from_date,to_date)).aggregate(Sum('amount'))['amount__sum'],
        'current_date':current_date,
        'hospital_instance':hospital_instance,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        }
        return render(request,'hospital/appointment_report.html',context=data)
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def generate_laboratory_reportView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST" and request.POST['from_date'] and request.POST['to_date']:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        from_date = request.POST['from_date'] 
        to_date = request.POST['to_date']  
        selected_lab_report=Labtest.objects.filter(hospital=hospital_instance,created_at__range=(from_date,to_date))
        current_date = datetime.date.today()
        data ={
        'selected_lab_report':selected_lab_report,
        'total_loboratory_cash':Labtest.objects.filter(hospital=hospital_instance,created_at__range=(from_date,to_date)).aggregate(Sum('amount'))['amount__sum'],
        'current_date':current_date,
        'hospital_instance':hospital_instance,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        }
        return render(request,'hospital/laboratory_report.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def generate_admission_reportView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST" and request.POST['from_date'] and request.POST['to_date']:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        from_date = request.POST['from_date'] 
        to_date = request.POST['to_date']  
        selected_lab_report=Admissionfees.objects.filter(hospital=hospital_instance,created_at__range=(from_date,to_date))
        current_date = datetime.date.today()
        data ={
        'selected_admission_report':selected_lab_report,
        'total_admission_cash':Admissionfees.objects.filter(hospital=hospital_instance,created_at__range=(from_date,to_date)).aggregate(Sum('amount'))['amount__sum'],
        'current_date':current_date,
        'hospital_instance':hospital_instance,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        }
        return render(request,'hospital/admission_report.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def generate_blood_bank_reportView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST" and request.POST['from_date'] and request.POST['to_date']:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        from_date = request.POST['from_date'] 
        to_date = request.POST['to_date']  
        selected_blood_bank_report=Bloodpurchase.objects.filter(hospital=hospital_instance,created_at__range=(from_date,to_date))
        current_date = datetime.date.today()
        data ={
        'selected_blood_bank_report':selected_blood_bank_report,
        'total_blood_bank_cash':Bloodpurchase.objects.filter(hospital=hospital_instance,created_at__range=(from_date,to_date)).aggregate(Sum('amount'))['amount__sum'],
        'current_date':current_date,
        'hospital_instance':hospital_instance,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),
        }
        return render(request,'hospital/blood_bank_report.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def generate_monthly_expenses_reportView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST" and request.POST['from_date'] and request.POST['to_date']:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        from_date = request.POST['from_date'] 
        to_date = request.POST['to_date']  
        selected_expenses_report=Expense.objects.filter(hospital=hospital_instance,created_at__range=(from_date,to_date))
        current_date = datetime.date.today()
        data ={
        'selected_expenses_report':selected_expenses_report,
        'total_expenses_cash':Expense.objects.filter(hospital=hospital_instance,created_at__range=(from_date,to_date)).aggregate(Sum('amount'))['amount__sum'],
        'current_date':current_date,
        'hospital_instance':hospital_instance,
        'app_message_count':Messages.objects.filter(hospital=hospital_instance,status=0).count(),

        }
        return render(request,'hospital/monthly_report.html',context=data)
    else:
        return redirect('/')