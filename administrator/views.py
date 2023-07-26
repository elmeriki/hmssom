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
from administrator.models import *
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

@login_required(login_url='/')  
def add_curency_listView(request):
    if request.user.is_authenticated and request.user.is_superuser: 
        data = {
            'curency_list':Curency.objects.all()
        }   
        return render(request,'superadmin/add_curency.html',context=data)
    else:
        return redirect('/')

@login_required(login_url='/')  
def add_curencyView(request):
    if request.user.is_authenticated and request.user.is_superuser:      
        return render(request,'superadmin/add_curency.html')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def delete_curencyView(request,id):
    if request.user.is_authenticated and request.user.is_superuser: 
        Curency.objects.filter(id=id).delete()     
        return redirect('/add_curency_list')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def create_curencyView(request):
    if request.user.is_authenticated and request.user.is_superuser and request.method=="POST":
        symbol = request.POST['symbol']
        desc = request.POST['desc']
        create_new_symbol=Curency(symbol=symbol,desc=desc)
        create_new_symbol.save()
        return redirect('/add_curency_list')
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def region_listView(request):
    if request.user.is_authenticated and request.user.is_superuser: 
        data = {
            'region_list':Region.objects.all()
        }   
        return render(request,'superadmin/region_list.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def add_regionView(request):
    if request.user.is_authenticated and request.user.is_superuser:      
        return render(request,'superadmin/region_list.html')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def create_regionView(request):
    if request.user.is_authenticated and request.user.is_superuser and request.method=="POST":
        name = request.POST['name']
        color = request.POST['color']
        create_new_region=Region(name=name,decolorsc=color)
        create_new_region.save()
        return redirect('/region_list')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def delete_regionView(request,id):
    if request.user.is_authenticated and request.user.is_superuser: 
        Region.objects.filter(id=id).delete()     
        return redirect('/region_list')
    else:
        return redirect('/')