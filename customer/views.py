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
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        medicine = request.POST['medicine']
        history = request.POST['history']
        note = request.POST['note']       
        advice = request.POST['advice']       
        id = random_id(length=9,character_set=string.digits)
        save_prescription_details=Prescription(hospital=hospital_instance, id=id, medicine=medicine, 
                                               history=history, note=note, advice=advice)
        save_prescription_details.save()
                                             
        messages.info(request,'Prescription created successfully')
        return redirect('/add_prescription')
    
       
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_prescriptionView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        return render(request,'customer/add_prescription.html')


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def prescription_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        all_prescription_list=Prescription.objects.filter(hospital=hospital_instance)
        prescription_data = {
            'all_prescription_list':all_prescription_list
        }
        return render(request,'customer/prescription_list.html',context=prescription_data )
    

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_appointmentView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
        return render(request,'customer/add_appointment.html',{})
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_appointmentView(request):
    #if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
    return render(request,'customer/add_appointment.html')

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def appointment_listView(request):
    #if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
    return render(request,'customer/appointment_list.html')
    

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def todays_appointmentView(request):
    #if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
    return render(request,'customer/todays_appointment.html')


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def upcoming_appointmentView(request):
    #if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
    return render(request,'customer/upcoming_appointment.html')


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def calendarView(request):
    #if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
    return render(request,'customer/calendar.html')


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def request_listView(request):
    #if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
    return render(request,'customer/request_appointment.html')