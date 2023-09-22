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
from administrator.models import *
from django.db.models import Sum
from random_id import random_id
import string 
import threading


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_medicinecategoryView(request):
    if request.user.is_authenticated and request.user.is_hospital:        
        return render(request,'customer/add_medicinecategory.html')
    else:
        return redirect('/')

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def medicinecategory_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)    
        data = {
            'medicine_category':Medicinecategory.objects.filter(hospital=hospital_instance)
        }    
        return render(request,'customer/medicinecategory_list.html',context=data)
    else:
        return redirect('/')
    

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_medicinecategoryView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        categoryname = request.POST['categoryname'] 
        desc = request.POST['desc'] 
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        create_new_medicine_category=Medicinecategory(hospital=hospital_instance,categoryname=categoryname,desc=desc)
        if create_new_medicine_category:
            create_new_medicine_category.save()
            messages.success(request,'Medicine Category created successfuly.')
            return redirect('/add_medicinecategory')
        else:
            return redirect('/add_medicinecategory')
            #messages.error(request,'Sorry, Medicine Category could not be created.')
    else:
        return redirect('/')


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_medicineView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        name = request.POST['name']
        category = int(request.POST['category'])
        storebox = request.POST['storebox']  
        purchaseprice = request.POST['purchaseprice']
        saleprice = request.POST['saleprice']
        quantity = request.POST['quantity']
        genericname = request.POST['genericname']  
        company = request.POST['company']
        effects = request.POST['effects'] 
        expiredate = request.POST['expiredate'] 
        username=request.user.username
        hospital_instance=User.objects.get(username=username) 
        category_instance=Medicinecategory.objects.get(id=category)
        save_new_medicine=Medicinal(hospital=hospital_instance, category=category_instance, name=name,storebox=storebox, purchaseprice=purchaseprice, saleprice=saleprice,
                                                quantity=quantity, genericname=genericname, company=company, effects=effects,expiredate=expiredate)
        if save_new_medicine:
            save_new_medicine.save()                                             
            messages.info(request,'Medicine has been saved successfully')
            return redirect('/add_medicine')
        else:
            return redirect('/')
    

def add_medicineView(request):
    if request.user.is_authenticated and request.user.is_hospital:  
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
        'all_medicine_categories':Medicinecategory.objects.filter(hospital=hospital_instance)
        }      
        return render(request,'customer/add_medicine.html',context=data)
    else:
        return redirect('/')
    

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def medicine_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        medicine_data = {
            'all_medicine_list': Medicinal.objects.filter(hospital=hospital_instance)
        }
        return render(request,'customer/medicine_list.html',context=medicine_data)
    else:
        return redirect('/')
    

# def medicine_by_categoryView(request,category):
#     if request.user.is_authenticated and request.user.is_hospital:
#         username=request.user.username
#         hospital_instance=User.objects.get(username=username)
#         if category == "Capsules":
#             list_all_capsules=Medicine.objects.filter(hospital=hospital_instance,category=category)
#             data = {
#                 'list_all_capsules':list_all_capsules
#             }
#             return render(request,'customer/medicine_list.html',context=data)
#         if category == "Liquid":
#             list_all_liquid=Medicine.objects.filter(hospital=hospital_instance,category=category)
#             data = {
#                 'list_all_liquid':list_all_liquid
#             }
#             return render(request,'customer/medicine_list.html',context=data)
#         if category == "Topical":
#             list_all_topical=Medicine.objects.filter(hospital=hospital_instance,category=category)
#             data = {
#                 'list_all_topical':list_all_topical
#             }
#             return render(request,'customer/medicine_list.html',context=data)
#         if category == "Injections":
#             list_all_injections=Medicine.objects.filter(hospital=hospital_instance,category=category)
#             data = {
#                 'list_all_injections':list_all_injections
#             }
#             return render(request,'customer/medicine_list.html',context=data)
        
#=======================================PRESCRIPTION====================================
        
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_prescriptionView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        phone =request.POST['phone']
        doctor_id =int(request.POST['doctor_id'])
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
            create_prescription=Prescription(hospital=hospital_instance,
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
def edit_prescriptionView(request,prescriptionid):
    if request.user.is_authenticated and request.user.is_hospital:
        get_prescription_instance = Prescription.objects.get(id=prescriptionid)
        data = {
        #'date':get_prescription_instance.date,
        'history':get_prescription_instance.history,
        'note':get_prescription_instance.note,
        'advice':get_prescription_instance.advice,
        'prescriptionid':get_prescription_instance.id,
        'prescriptionid':prescriptionid
        }
        return render(request,'customer/edit_prescription.html',context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_prescriptionView(request,prescriptionid):
    if request.user.is_authenticated and request.user.is_hospital:
        history=request.POST['history']
        note=request.POST['note']
        advice=request.POST['advice']
        Prescription.objects.filter(pk=prescriptionid).update(history=history)
        Prescription.objects.filter(pk=prescriptionid).update(note=note)
        Prescription.objects.filter(pk=prescriptionid).update(advice=advice)
        messages.info(request,'Update has been done successfully')
        return redirect(f'/edit_prescription/{prescriptionid}')


@login_required(login_url='/')  
def delete_prescriptionView(request, prescriptionid):
    if request.user.is_authenticated and request.user.is_hospital:
        delete_prescription = Prescription.objects.get(id=prescriptionid)
        delete_prescription.delete()
        return redirect('/prescription_list')
    
#=======================================APPOINTMENT====================================
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
        'doctor_list':Doctor.objects.filter(hospital=hospital_instance,status=0),
        'appointment_list':Appointmentfees.objects.all()
        }
        return render(request,'customer/add_appointment.html',context=data)
    
    if request.user.is_authenticated and request.user.is_rep:     
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)       
        data= {
        'doctor_list':Doctor.objects.filter(hospital=hospital_instance,status=0),
        'appointment_list':Appointmentfees.objects.all(),
        }
        return render(request,'receptionist/add_appointment.html',context=data)
    
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_appointment_View(request,patient_id):
    if request.user.is_authenticated and request.user.is_hospital:     
        username=request.user.username
        hospital_instance=User.objects.get(username=username)        
        data= {
        'doctor_list':Doctor.objects.filter(hospital=hospital_instance,status=0),
        'appointment_list':Appointmentfees.objects.all(),
        'patient_id':patient_id
        }
        return render(request,'customer/add_appointment.html',context=data)
    
    if request.user.is_authenticated and request.user.is_rep:     
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)       
        data= {
        'doctor_list':Doctor.objects.filter(hospital=hospital_instance,status=0),
        'appointment_list':Appointmentfees.objects.all(),
        'patient_id':patient_id
        }
        return render(request,'receptionist/add_appointment.html',context=data)
    
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
        patient_instance=Patient.objects.get(phone=phone)
        hospital_instance=User.objects.get(username=username) 
        
        if Appointment.objects.filter(patient=patient_instance,hospital=hospital_instance).filter(status=0).exists():
            messages.info(request,'Please cancel first Appointment before you can create another Appointment')
            return redirect('/add_appointment')
        else:
            doctor_instance=Doctor.objects.get(id=doctor_id)
            create_apointment=Appointment(hospital=hospital_instance,date=apointmentdate,patient=patient_instance,dr=doctor_instance,visitdsc=visitdesc,remark=remarks,amount=charges,paymenttype=paymenttype,paymentstatus=payment_status) 
            create_apointment.save()
            messages.info(request,'Patient Appointment has been created successfully')
            return redirect('/add_appointment')
    if request.user.is_authenticated and request.user.is_rep and request.method=="POST":
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
        patient_instance=Patient.objects.get(phone=phone)
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username) 
        if Appointment.objects.filter(patient=patient_instance,hospital=hospital_instance).filter(status=0).exists():
            messages.info(request,'Please cancel first Appointment before you can create another Appointment')
            return redirect('/add_appointment')
        else:
            doctor_instance=Doctor.objects.get(id=doctor_id)
            create_apointment=Appointment(hospital=hospital_instance,date=apointmentdate,patient=patient_instance,dr=doctor_instance,visitdsc=visitdesc,remark=remarks,amount=charges,paymenttype=paymenttype,paymentstatus=payment_status) 
            create_apointment.save()
            messages.info(request,'Patient Appointment has been created successfully')
            return redirect('/add_appointment')
    else:
        return redirect('/')

@login_required(login_url='/')  
def appointment_listView(request):
    if request.user.is_authenticated and request.user.is_hospital: 
        username=request.user.username
        hospital_instance=User.objects.get(username=username) 
        data = {
        'appointment_list':Appointment.objects.filter(hospital=hospital_instance)
        }       
        return render(request,'customer/appointment_list.html',context=data)
    
    if request.user.is_authenticated and request.user.is_rep: 
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        data = {
        'appointment_list':Appointment.objects.filter(hospital=hospital_instance)
        }       
        return render(request,'receptionist/appointment_list.html',context=data)
    else:
        return redirect('/')
    

@login_required(login_url='/')  
def edit_appointmentView(request,appointmentid):
    if request.user.is_authenticated and request.user.is_hospital:
        get_appointment_instance = Appointment.objects.get(id=appointmentid)
        data = {
        'phone' : get_appointment_instance.patient.phone,
        'date' : get_appointment_instance.date,
        'amount' : get_appointment_instance.amount,
        'remark' : get_appointment_instance.remark,
        'visitdsc' : get_appointment_instance.visitdsc,
        'paymenttype': get_appointment_instance.paymenttype,
        'status' : get_appointment_instance.status,
        'appointmentid':get_appointment_instance.id,
        'appointmentid':appointmentid,

        }
        return render(request,'customer/edit_appointment.html',context=data)


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_appointmentView(request,appointmentid):
    if request.user.is_authenticated and request.user.is_hospital:
        phone =request.POST['phone']
        #doctor_id =int(request.POST['doctor_id'])
        apointmentdate =request.POST['apointmentdate']
        charges =request.POST['charges']
        remarks =request.POST['remarks']
        visitdesc =request.POST['visitdesc'] 
        paymenttype =request.POST['paymenttype'] 
        payment_status =request.POST['payment_status'] 

        
        Appointment.objects.filter(pk=appointmentid).update(phone=phone)
        #Appointment.objects.filter(pk=appointmentid).update(doctor_id=doctor_id)
        Appointment.objects.filter(pk=appointmentid).update(date=apointmentdate)
        Appointment.objects.filter(pk=appointmentid).update(amount=charges)
        Appointment.objects.filter(pk=appointmentid).update(remark=remarks)
        Appointment.objects.filter(pk=appointmentid).update(visitdsc=visitdesc)
        Appointment.objects.filter(pk=appointmentid).update(paymenttype=paymenttype)
        Appointment.objects.filter(pk=appointmentid).update(status=payment_status)
        messages.info(request,'Update has been done successfully')

        return redirect(f'/edit_appointment/{appointmentid}')


@login_required(login_url='/')  
def delete_appointmentView(request, appointmentid):
    if request.user.is_authenticated and request.user.is_hospital:
        delete_appointment = Appointment.objects.get(id=appointmentid)
        delete_appointment.delete()
        return redirect('/appointment_list')


    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def todays_appointment_listView(request):
    if request.user.is_authenticated and request.user.is_hospital or request.user.is_authenticated and request.user.is_dr: 
        todays_date = date.today()
        username=request.user.username
        hospital_instance=User.objects.get(username=username) 
        data = {
        'todaysappointment_list':Appointment.objects.filter(hospital=hospital_instance,date=todays_date)
        }       
        return render(request,'customer/appointment_list.html',context=data)
    if request.user.is_authenticated and request.user.is_rep: 
        todays_date = date.today()
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        data = {
        'todaysappointment_list':Appointment.objects.filter(hospital=hospital_instance,date=todays_date)
        }       
        return render(request,'receptionist/appointment_list.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def upcoming_appointment_listView(request):
    if request.user.is_authenticated and request.user.is_hospital or request.user.is_authenticated and request.user.is_dr: 
        todays_date = date.today()
        username=request.user.username
        hospital_instance=User.objects.get(username=username) 
        data = {
        'todaysappointment_list':Appointment.objects.filter(hospital=hospital_instance,date__gt=todays_date)
        }       
        return render(request,'customer/appointment_list.html',context=data)
    if request.user.is_authenticated and request.user.is_rep: 
        todays_date = date.today()
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)
        data = {
        'todaysappointment_list':Appointment.objects.filter(hospital=hospital_instance,date__gt=todays_date)
        }       
        return render(request,'receptionist/appointment_list.html',context=data)
    else:
        return redirect('/')
    
    
    
def app_homeView(request):
    data = {
        'region_list':Region.objects.all()
    }
    return render(request,'app/index.html',context=data)

def book_nowView(request,hospital_id):
    data = {
        'hospital_id':hospital_id
    }
    return render(request,'app/book.html',context=data)

def app_hospital_detailView(request,hospital_id):
    hospital_detail = User.objects.get(id=hospital_id)
    data = {
        'hospital_id':hospital_id,
        'hospital_detail':hospital_detail,
        'hospital_more_detail':Hospital.objects.get(hospital=hospital_detail),
        'hospital_doctors_count':Doctor.objects.filter(hospital=hospital_detail).count(),
        'hospital_staff_count':Humanresource.objects.filter(hospital=hospital_detail).count(),
        'hospital_treated_count':Treatment.objects.filter(hospital=hospital_detail).count()
    }
    return render(request,'app/hospital_detail.html',context=data)


def create_book_nowView(request,hospital_id):
    if request.method=="POST" and request.POST['cellphone'] and request.POST['names'] and request.POST['message'] and request.POST['checks']:
        cellphone = request.POST['cellphone']
        names = request.POST['names']
        message = request.POST['message']
        checks = int(request.POST['checks'])
        hospital_instance=User.objects.get(id=hospital_id)
        
        if  Messages.objects.filter(hospital=hospital_instance,phone=cellphone).filter(status=0).exists():
            messages.success(request,'Your previous booking is pending')
            return redirect(f'/book_now/{hospital_id}') 
            
        if not checks == 2:
            messages.success(request,'Incorrect security checks')
            return redirect(f'/book_now/{hospital_id}')
        else:
            create_new_booking=Messages(hospital=hospital_instance,names=names,phone=cellphone,message=message)
            create_new_booking.save()  
            messages.success(request,'You request has been sent successfully.')
            return redirect(f'/book_now/{hospital_id}')
    else:
        return redirect(f'/app_home')
    
    
def app_query_searchView(request):
    if request.method=="POST" and request.POST['query']:
        query = request.POST['query']
        hospital_list_base_on_city=User.objects.filter(is_hospital=True).filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        data={
        'hospital_list_base_on_city':hospital_list_base_on_city 
        }
        return render(request,'app/hospital_search.html',context=data)
    else:
        return redirect(f'/app_home')
    
            
def app_loginView(request):
    return render(request,'app/login.html')


def app_registerView(request):
    return render(request,'app/register.html')

def app_hospital_listView(request,city_names):
    data = {
        'hospital_list_base_on_city':User.objects.filter(city=city_names)
    }
    return render(request,'app/hospital_list.html',context=data)