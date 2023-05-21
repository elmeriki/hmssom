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


@login_required(login_url='/')  
def hospital_dashboardView(request):
    return render(request,'hospital/dashboard.html')
    


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
            return redirect('/department')
        else:
            return redirect('/department')
    else:
       return redirect('/department')
    


@login_required(login_url='/')  
def edit_departmentView(request, pk):
    if request.user.is_authenticated and request.user.is_hospital:
        #fetching data of particular id
        get_data = Department.objects.get(id=pk)
        return render(request,'hospital/edit_department.html', {'department_data': get_data})


@login_required(login_url='/')  
def update_departmentView(request, pk):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        #updating  data of particular id
        update_data = Department.objects.get(id=pk)
        update_data.name = request.POST['departmentname']
        update_data.desc = request.POST['departmentdec']
        #query save method
        update_data.save()
        #render to department page
        return redirect('/department')


@login_required(login_url='/')  
def delete_departmentView(request, pk):
    if request.user.is_authenticated and request.user.is_hospital:
        #delete  data of particular id
        del_data = Department.objects.get(id=pk)
        #query delete method
        del_data.delete()
        return redirect('/department')




#@login_required(login_url='/')  
def doctor_listView(request):
        return render(request,'hospital/doctor_list.html')
        
def patient_listView(request):
    return render(request,'hospital/patient_list.html')