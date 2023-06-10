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
def add_paymentView(request):
    #if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
    return render(request,'finance/add_payment.html')

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def payment_listView(request):
    #if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
    return render(request,'finance/payment_list.html')

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_paymentcategoryView(request):
    #if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
    return render(request,'finance/add_paymentcategory.html')


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def paymentcategoryView(request):
    #if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
    return render(request,'finance/paymentcategory.html')
    
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_expenseView(request):
    #if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
    return render(request,'finance/add_expense.html')

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def expense_listView(request):
    #if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
    return render(request,'finance/expense_list.html')

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_expensecategoryView(request):
    #if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
    return render(request,'finance/add_expensecategory.html')


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def expensecategoryView(request):
    #if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
    return render(request,'finance/expensecategory.html')
    