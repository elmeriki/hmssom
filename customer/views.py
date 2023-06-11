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
@transaction.atomic  #transactional 
def create_medicineView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        name = request.POST['name']
        category = request.POST['category']
        storebox = request.POST['storebox']  
        purchaseprice = request.POST['purchaseprice']
        saleprice = request.POST['saleprice']
        quantity = request.POST['quantity']
        genericname = request.POST['genericname']  
        company = request.POST['company']
        effects = request.POST['effects']      
        id = random_id(length=9,character_set=string.digits)
        save_medicine_details=Medicine(hospital=hospital_instance, id=id, name=name, category=category,
                                                storebox=storebox, purchaseprice=purchaseprice, saleprice=saleprice,
                                                quantity=quantity, genericname=genericname, company=company, effects=effects)
        save_medicine_details.save()
                                             
        messages.info(request,'Medicine created successfully')
        return redirect('/add_medicine')
    
       
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_medicineView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        return render(request,'customer/add_medicine.html')


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def medicine_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        all_medicine_list=Medicine.objects.filter(hospital=hospital_instance)
        medicine_data = {
            'all_medicine_list':all_medicine_list
        }
        return render(request,'customer/medicine_list.html',context=medicine_data)
    

def medicine_by_categoryView(request,category):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        if category == "Capsules":
            list_all_capsules=Medicine.objects.filter(hospital=hospital_instance,category=category)
            data = {
                'list_all_capsules':list_all_capsules
            }
            return render(request,'customer/medicine_list.html',context=data)
        if category == "Liquid":
            list_all_liquid=Medicine.objects.filter(hospital=hospital_instance,category=category)
            data = {
                'list_all_liquid':list_all_liquid
            }
            return render(request,'customer/medicine_list.html',context=data)
        if category == "Topical":
            list_all_topical=Medicine.objects.filter(hospital=hospital_instance,category=category)
            data = {
                'list_all_topical':list_all_topical
            }
            return render(request,'customer/medicine_list.html',context=data)
        if category == "Injections":
            list_all_injections=Medicine.objects.filter(hospital=hospital_instance,category=category)
            data = {
                'list_all_injections':list_all_injections
            }
            return render(request,'customer/medicine_list.html',context=data)
        
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_prescriptionView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        phone =request.POST['phone']
        doctor_id =int(request.POST['doctor_id'])
        prescriptiondate =request.POST['date']
        history = request.POST['history']
        note = request.POST['note']
        advice = request.POST['advice']
        username=request.user.username
        if not Patient.objects.filter(phone=phone).exists():
            messages.info(request,'Patient Cellphone Number Does Not Exists')
            return redirect('/add_prescription')
        else:
            hospital_instance=User.objects.get(username=username)   
            patient_instance=Patient.objects.get(phone=phone)
            doctor_instance=Doctor.objects.get(id=doctor_id)
            create_prescription=Prescription(hospital=hospital_instance,date=prescriptiondate,
                                             patient=patient_instance,dr=doctor_instance,history=history,
                                             note=note,advice=advice) 
            create_prescription.save()
            messages.info(request,'Patient Prescription has been created successfully')
            return redirect('/add_prescription')
    else:
        return redirect('/')
       

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_prescriptionView(request):
    if request.user.is_authenticated and request.user.is_hospital:     
        username=request.user.username
        hospital_instance=User.objects.get(username=username)        
        data= {
        'doctor_list':Doctor.objects.filter(hospital=hospital_instance,status=0)
        }
        return render(request,'customer/add_prescription.html', context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def prescription_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        all_prescription_list=Prescription.objects.filter(hospital=hospital_instance)
        data = {
            'all_prescription_list':all_prescription_list
        }
        return render(request,'customer/prescription_list.html',context=data )
    else:
        return redirect('/')
    

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_appointmentView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
        return render(request,'customer/add_appointment.html',{})
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_appointmentView(request):
    if request.user.is_authenticated and request.user.is_hospital:     
        username=request.user.username
        hospital_instance=User.objects.get(username=username)        
        data= {
        'doctor_list':Doctor.objects.filter(hospital=hospital_instance,status=0)
        }
        return render(request,'customer/add_appointment.html',context=data)
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_patient_appointmentView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        phone =request.POST['phone']
        doctor_id =int(request.POST['doctor_id'])
        apointmentdate =request.POST['apointmentdate']
        charges =request.POST['charges']
        remarks =request.POST['remarks']
        visitdesc =request.POST['visitdesc'] 
        paymenttype =request.POST['paymenttype'] 
        payment_status =request.POST['payment_status'] 
        username=request.user.username
        if not Patient.objects.filter(phone=phone).exists():
            messages.info(request,'Patient Cellphone Number Does Not Exists')
            return redirect('/add_appointment')
        else:
            hospital_instance=User.objects.get(username=username)   
            patient_instance=Patient.objects.get(phone=phone)
            doctor_instance=Doctor.objects.get(id=doctor_id)
            create_apointment=Appointment(hospital=hospital_instance,date=apointmentdate,patient=patient_instance,dr=doctor_instance,visitdsc=visitdesc,remark=remarks,amount=charges,paymenttype=paymenttype,paymentstatus=payment_status) 
            create_apointment.save()
            messages.info(request,'Patient Appointment has been created successfully')
            return redirect('/add_appointment')
    else:
        return redirect('/')

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def appointment_listView(request):
    if request.user.is_authenticated and request.user.is_hospital: 
        username=request.user.username
        hospital_instance=User.objects.get(username=username) 
        data = {
        'appointment_list':Appointment.objects.filter(hospital=hospital_instance)
        }       
        return render(request,'customer/appointment_list.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def todays_appointment_listView(request):
    if request.user.is_authenticated and request.user.is_hospital: 
        todays_date = date.today()
        username=request.user.username
        hospital_instance=User.objects.get(username=username) 
        data = {
        'todaysappointment_list':Appointment.objects.filter(hospital=hospital_instance,date=todays_date)
        }       
        return render(request,'customer/appointment_list.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def upcoming_appointment_listView(request):
    if request.user.is_authenticated and request.user.is_hospital: 
        todays_date = date.today()
        username=request.user.username
        hospital_instance=User.objects.get(username=username) 
        data = {
        'todaysappointment_list':Appointment.objects.filter(hospital=hospital_instance,date__gt=todays_date)
        }       
        return render(request,'customer/appointment_list.html',context=data)
    else:
        return redirect('/')