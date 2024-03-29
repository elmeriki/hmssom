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
from finance.models import *
from django.db.models import Sum
from random_id import random_id
import string 
import threading


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_paymentView(request,patien_id):
    if request.user.is_authenticated and request.user.is_hospital:    
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        patien_instance=Patient.objects.get(phone=patien_id) 
        data={
        'patien_id':patien_id,
        'patient_test_list':Patienttest.objects.filter(patient=patien_instance,hospital=hospital_instance).filter(status=1),
        'total_sum_of_test':Patienttest.objects.filter(patient=patien_instance,hospital=hospital_instance).filter(status=1).aggregate(Sum('amount'))['amount__sum']
        }    
        return render(request,'finance/add_payment.html',context=data)

    if request.user.is_authenticated and request.user.is_rep:    
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=doctor_instance.hospital.username)
        patien_instance=Patient.objects.get(phone=patien_id) 
        data={
        'patien_id':patien_id,
        'patient_test_list':Patienttest.objects.filter(patient=patien_instance,hospital=hospital_instance).filter(status=1),
        'total_sum_of_test':Patienttest.objects.filter(patient=patien_instance,hospital=hospital_instance).filter(status=1).aggregate(Sum('amount'))['amount__sum']
        }    
        return render(request,'receptionist/add_payment.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def payment_listView(request):
    if request.user.is_authenticated and request.user.is_hospital: 
        username=request.user.username
        hospital_instance=User.objects.get(username=username)  
        data = {
         'payment_list':Payment.objects.filter(hospital=hospital_instance)[:10],
         'hospital_instance':hospital_instance
        }       
        return render(request,'finance/payment_list.html',context=data)
    if request.user.is_authenticated and request.user.is_rep: 
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)   
        data = {
         'payment_list':Payment.objects.filter(hospital=hospital_instance)[:10],
         'hospital_instance':hospital_instance
        }       
        return render(request,'receptionist/payment_list.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_paymentcategoryView(request):
    if request.user.is_authenticated and request.user.is_hospital:        
        return render(request,'finance/add_paymentcategory.html')
    
    if request.user.is_authenticated and request.user.is_rep:        
        return render(request,'receptionist/add_paymentcategory.html')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_appointment_feesView(request):
    if request.user.is_authenticated and request.user.is_hospital:  
              
        return render(request,'finance/add_appointment_fees.html')
    else:
        return redirect('/')

@login_required(login_url='/')  
def paymentcategoryView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)    
        data = {
            'payment_category':Paymentcategory.objects.filter(hospital=hospital_instance)
        }    
        return render(request,'finance/paymentcategory.html',context=data)
    if request.user.is_authenticated and request.user.is_rep:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)    
        data = {
            'payment_category':Paymentcategory.objects.filter(hospital=hospital_instance)
        }    
        return render(request,'receptionist/paymentcategory.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def appointment_categoryView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)    
        data = {
            'payment_category':Appointmentfees.objects.filter(hospital=hospital_instance),
            'hospital_instance':hospital_instance
        }    
        return render(request,'finance/appointment_payment_list.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def delete_appointment_payment_categoryView(request,id):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)    
        Appointmentfees.objects.filter(id=id,hospital=hospital_instance).delete()
        return redirect('/appointment_category')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_expenseView(request):
    if request.user.is_authenticated and request.user.is_hospital:  
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
        'all_expenses_categories':Expensescategory.objects.filter(hospital=hospital_instance)
        }      
        return render(request,'finance/add_expense.html',context=data)
    if request.user.is_authenticated and request.user.is_rep:  
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username) 
        data = {
        'all_expenses_categories':Expensescategory.objects.filter(hospital=hospital_instance)
        }      
        return render(request,'receptionist/add_expense.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def expense_listView(request):
    if request.user.is_authenticated and request.user.is_hospital: 
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = { 
        'expenses_list':Expense.objects.filter(hospital=hospital_instance)[:15],
        'hospital_instance':hospital_instance
        }       
        return render(request,'finance/expense_list.html',context=data)
    if request.user.is_authenticated and request.user.is_rep: 
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username) 
        data = { 
        'expenses_list':Expense.objects.filter(hospital=hospital_instance)[:15],
        'hospital_instance':hospital_instance
        }       
        return render(request,'finance/expense_list.html',context=data)
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def admision_feesView(request):
    if request.user.is_authenticated and request.user.is_hospital: 
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = { 
        'admission_fees':Admissionfees.objects.filter(hospital=hospital_instance),
        'hospital_instance':hospital_instance
        }       
        return render(request,'finance/admision_fees.html',context=data)
    else:
        return redirect('/')

    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_expensecategoryView(request):
    if request.user.is_authenticated and request.user.is_hospital:        
        return render(request,'finance/add_expensecategory.html')
    else:
        return redirect('/')

@login_required(login_url='/')  
def expensecategoryView(request):
    if request.user.is_authenticated and request.user.is_hospital:  
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        data = {
        'expenses_categories':Expensescategory.objects.filter(hospital=hospital_instance)
        }      
        return render(request,'finance/expensecategory.html',context=data)
    if request.user.is_authenticated and request.user.is_rep:  
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        recep_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=recep_instance.hospital.username)  
        data = {
        'expenses_categories':Expensescategory.objects.filter(hospital=hospital_instance)
        }      
        return render(request,'receptionist/expensecategory.html',context=data)
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def admission_feesView(request,patient_id,price):
    if request.user.is_authenticated and request.user.is_hospital:  
        from datetime import datetime, timedelta
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        patient_instance =Patient.objects.get(phone=patient_id)
        data = {
        'price':price,
        'patient_id':patient_id,
        'patient_instance':patient_instance,
        'hospital_instance':hospital_instance,
        }
        return render(request,'finance/admision_fees.html',context=data)
    if request.user.is_authenticated and request.user.is_rep:  
        from datetime import datetime, timedelta
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        patient_instance =Patient.objects.get(phone=patient_id)
        data = {
        'price':price,
        'patient_id':patient_id,
        'patient_instance':patient_instance,
        'hospital_instance':hospital_instance,
        }
        return render(request,'receptionist/admision_fees.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def save_admission_feesView(request):
    if request.user.is_authenticated and request.user.is_hospital or request.user.is_rep and request.method=="POST":
        patientid =request.POST['patientid']
        price =int(request.POST['price'])
        days =int(request.POST['days'])
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        patient_instance =Patient.objects.get(phone=patientid)
        total_cost =price * days
        save_admision_fees=Admissionfees(hospital=hospital_instance,patient=patient_instance,days=days,amount=total_cost,paymenttype=1)
        if save_admision_fees:
            save_admision_fees.save()
            Admission.objects.filter(hospital=hospital_instance,patient=patient_instance).update(status="1")
        return redirect('/all_admission')
    if request.user.is_authenticated and request.user.is_rep and request.method=="POST":
        patientid =request.POST['patientid']
        price =int(request.POST['price'])
        days =int(request.POST['days'])
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        patient_instance =Patient.objects.get(phone=patientid)
        total_cost =price * days
        save_admision_fees=Admissionfees(hospital=hospital_instance,patient=patient_instance,days=days,amount=total_cost,paymenttype=1)
        if save_admision_fees:
            save_admision_fees.save()
            Admission.objects.filter(hospital=hospital_instance,patient=patient_instance).update(status="1")
        return redirect('/all_admission')
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_new_categoryView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        category_name =request.POST['category']  
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        create_new_expenses_category=Expensescategory(hospital=hospital_instance,name=category_name)
        if create_new_expenses_category:
            create_new_expenses_category.save()
            messages.success(request,'Expended Category created successfuly.')
            return redirect('/add_expensecategory')
        else:
            return redirect('/add_expensecategory')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_new_expensesView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        category_id =int(request.POST['category'] )
        amount =request.POST['amount'] 
        desc =request.POST['description']  
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        category_instance = Expensescategory.objects.get(id=category_id)
        save_new_expenses=Expense(hospital=hospital_instance,category=category_instance,amount=amount,decs=desc)
        if save_new_expenses:
            save_new_expenses.save()
            messages.success(request,'Expenses has been save successfuly.')
            return redirect('/add_expense')
        else:
            return redirect('/add_expense')
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_new_payment_categoryView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        category_name =request.POST['category']  
        description =request.POST['description']  
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        create_new_payment_category=Paymentcategory(hospital=hospital_instance,category=category_name,amount=description)
        if create_new_payment_category:
            create_new_payment_category.save()
            messages.success(request,'Payment Category created successfuly.')
            return redirect('/add_paymentcategory')
        else:
            return redirect('/add_paymentcategory')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_new_appointment_categoryView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        category_name =request.POST['category']  
        amount =request.POST['amount']  
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        create_new_appointment_category=Appointmentfees(hospital=hospital_instance,category=category_name,amount=amount)
        if create_new_appointment_category:
            create_new_appointment_category.save()
            # messages.success(request,'Appointment Fees has been created successfuly.')
            return redirect('/appointment_category')
        else:
            return redirect('/appointment_category')
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def record_paymentView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        phone =request.POST['phone']
        amount =request.POST['amount']
        paymenttype =request.POST['paymenttype'] 
        payment_status =request.POST['payment_status'] 
        username=request.user.username
        hospital_instance=User.objects.get(username=username)   
        patient_instance=Patient.objects.get(phone=phone)
        if Payment.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(paymentstatus="Pending").exists():
            messages.info(request,'Previous Payment has not been settle.')
            return redirect(f'/add_payment/{phone}')
        else:
            save_new_payment=Payment(hospital=hospital_instance,patient=patient_instance,category="Lab Test",amount=amount,paymenttype=paymenttype,paymentstatus=payment_status) 
            save_new_payment.save()
            existing_test_id=Treatment.objects.filter(hospital=hospital_instance,payment="Pending").values_list('treatmentid', flat=True).get(patient=patient_instance)
            Treatment.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(payment="Pending").update(payment=payment_status)
            create_lap_report=Lapreport(hospital=hospital_instance,patient=patient_instance,status="Processing",testid=existing_test_id)
            create_lap_report.save()
            return redirect(f'/treatment_list')
    if request.user.is_authenticated and request.user.is_rep and request.method=="POST":
        phone =request.POST['phone']
        amount =request.POST['amount']
        paymenttype =request.POST['paymenttype'] 
        payment_status =request.POST['payment_status'] 
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        doctor_instance=Doctor.objects.get(user=customer_instance)
        hospital_instance=User.objects.get(username=doctor_instance.hospital.username) 
        patient_instance=Patient.objects.get(phone=phone)
        if Payment.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(paymentstatus="Pending").exists():
            messages.info(request,'Previous Payment has not been settle.')
            return redirect(f'/add_payment/{phone}')
        else:
            save_new_payment=Payment(hospital=hospital_instance,patient=patient_instance,category="Lab Test",amount=amount,paymenttype=paymenttype,paymentstatus=payment_status) 
            save_new_payment.save()
            existing_test_id=Treatment.objects.filter(hospital=hospital_instance,payment="Pending").values_list('treatmentid', flat=True).get(patient=patient_instance)
            Treatment.objects.filter(hospital=hospital_instance,patient=patient_instance).filter(payment="Pending").update(payment=payment_status)
            create_lap_report=Lapreport(hospital=hospital_instance,patient=patient_instance,status="Processing",testid=existing_test_id)
            create_lap_report.save()
            return redirect(f'/treatment_list')
    else:
        return redirect('/')