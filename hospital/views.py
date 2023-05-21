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
from django.db.models import Sum
from random_id import random_id
import string 
import threading

@login_required(login_url='/')  
def hospital_dashboardView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
        'count_number_of_patient':Patient.objects.filter(hospital=hospital_instance).count(),
        'count_number_of_doctors':Doctor.objects.filter(hospital=hospital_instance).count()
        }
        return render(request,'hospital/dashboard.html',context=data)
    


@login_required(login_url='/')  
def departmentView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        hospital_department =Department.objects.filter(hospital=hospital_instance)
        data = {
        'hospital_department':hospital_department
        }
        return render(request,'hospital/department.html',context=data)
    
    
@login_required(login_url='/')  
def add_departmentView(request):
    return render(request,'hospital/add_department.html')


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def save_add_departmentView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        department_name = request.POST['departmentname']
        department_decs = request.POST['departmentdec']
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        create_Department =Department(hospital=hospital_instance,name=department_name,desc=department_decs)
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
        data = {
        'department':get_department_instance.name,
        'deaprtmentdesc':get_department_instance.desc,
        'departmentid':get_department_instance.id,
        'departmentid':departmentid
        }
        return render(request,'hospital/edit_department.html',context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_departmentView(request,departmentid):
    if request.user.is_authenticated and request.user.is_hospital:
        departmentname=request.POST['departmentname']
        departmentdec=request.POST['departmentdec']
        Department.objects.filter(pk=departmentid).update(name=departmentname)
        Department.objects.filter(pk=departmentid).update(desc=departmentdec)
        messages.info(request,'Update has been done successfully')
        return redirect(f'/edit_department/{departmentid}')


@login_required(login_url='/')  
def delete_departmentView(request, departmentid):
    if request.user.is_authenticated and request.user.is_hospital:
        delete_department = Department.objects.get(id=departmentid)
        delete_department.delete()
        return redirect('/department')
    


@login_required(login_url='/')  
def doctor_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        all_doctors_list =Doctor.objects.filter(hospital=hospital_instance)
        data = {
            'all_doctors_list':all_doctors_list
        }
        return render(request,'hospital/doctor_list.html',context=data)
    
    
@login_required(login_url='/')  
def add_doctorView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        get_all_hospital_department_list = Department.objects.filter(hospital=hospital_instance)
        data = {
            'get_all_hospital_department_list':get_all_hospital_department_list
        }
        return render(request,'hospital/add_doctor.html',context=data)
        
def patient_listView(request):
    return render(request,'hospital/patient_list.html')


    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_doctorView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
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
        email = request.POST['email']
        number = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        departmentid = request.POST['department']
        message_about_dr = request.POST['message_about_dr']
        doctorsid = random_id(length=9,character_set=string.digits)
        department_instance = Department.objects.get(id=departmentid)
        create_new_doctors_account=User.objects.create_user(username=email,first_name=name,last_name=name,password=password,is_dr=True,email=email,address=address,number=number,customerid=doctorsid)
        create_new_doctors_account.save()
            
        save_doctors_details=Doctor(user=create_new_doctors_account,hospital=hospital_instance,department=department_instance,name=name,email=email,phone=number,address=address,signature=signature,picture=picture,profile=message_about_dr)
        save_doctors_details.save()
        messages.info(request,'Doctors Profile created successfully')
        return render(request,'hospital/add_doctor.html',{})
    

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_patientView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        title = request.POST['title']
        patientname = request.POST['patientname']
        nok = request.POST['nok']
        non = request.POST['non']
        number = request.POST['phone']        
        paymenttype = request.POST['paymenttype']
        patientid = random_id(length=9,character_set=string.digits)
    
        save_patient_details=Patient(hospital=hospital_instance,patientid=patientid,title=title,name=patientname,nok=nok,non=non,phone=number,paymenttype=paymenttype)
        save_patient_details.save()
        messages.info(request,'Patient Profile created successfully')
        return redirect('/add_patient')
    

@login_required(login_url='/')  
def add_patientView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        return render(request,'hospital/add_patient.html')
    
        
def patient_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        list_all_patient =Patient.objects.filter(hospital=hospital_instance)
        data = {
            'list_all_patient':list_all_patient
        }
        return render(request,'hospital/patient_list.html',context=data)
    
    
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
        title = request.POST['title']
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        number = request.POST['phone']        
        employeeid = random_id(length=10,character_set=string.digits)
    
        save_humanresource_details=Humanresource(hospital=hospital_instance, employeeid=employeeid,title=title,name=name,email=email,address=address,phone=number,signature=signature,picture=picture)
        save_humanresource_details.save()
        messages.info(request,'Employee Profile created successfully')
        return redirect('/add_human_resource')

   
@login_required(login_url='/')  
def add_humanresourceView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        return render(request,'hospital/add_human_resource.html')
    
    
def humanresource_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        list_all_humanresource=Humanresource.objects.filter(hospital=hospital_instance)
        hr_data = {
            'list_all_humanresource':list_all_humanresource 
        }
        return render(request,'hospital/human_resource_list.html',context=hr_data)