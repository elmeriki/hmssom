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
# Create your views here.


class Emailthread(threading.Thread):
    def __init__(self,msg):
        self.msg=msg
        threading.Thread.__init__(self)
    def run(self):
        self.msg.send(fail_silently=False)
        

def welcomeView(request):
    return render(request,'hospital/login.html',context={})


def hospital_loginView(request):
    return render(request,'hospital/login.html')
    

def register_loginView(request):
    return render(request,'hospital/register.html')

def logoutView(request):
    auth.logout(request)
    messages.info(request,"Logout Successfully")
    return redirect('/') 


def hospital_login_View(request):
    if request.method =="POST" and request.POST['username'] and request.POST['password']:
        username = request.POST['username']
        password =request.POST['password']
                
        if not User.objects.filter(username=username).exists():
            messages.info(request,'Incorrect credentials.')
            return redirect('/')  
        
        userlog = auth.authenticate(username=username,password=password)
        # checking if it is an existing user in the database
        
        # customise error messages handler
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_hospital:
                return redirect('/hospital_dashboard')
        else:
            messages.info(request,"Incorrect credentials.")
            return redirect('/')
                
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and not request.user.is_activation:
                messages.info(request,"Account is not yet activated")
                return redirect('/')
            
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_dr:
                return redirect('/')
        else:
            messages.info(request,"Incorrect credentials.")
            return redirect('/')
            
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_admin:
                return redirect('/')
        else:
            messages.info(request,"Incorrect credentials.")
            return redirect('/')
            
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_cashier:
                return redirect('/')
            
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_supervisor:
                return redirect('/')
            
            else:
                messages.info(request,"Incorrect credentials.")
                return redirect('/')
    else:
        return redirect('/')  


@transaction.atomic  #transactional 
def create_hospital_accountView(request):
    if request.method == "POST":
        hospital_name = request.POST['hospitalname']
        email = request.POST['email']
        address = request.POST['address']
        number = request.POST['number']
        package = request.POST['package']
        remarks = request.POST['remarks']
        country = request.POST['country']
        
        if User.objects.filter(email=email).exists():
            messages.info(request,'Email has been used already.')
            return redirect('/register_hospital')  
        
        if User.objects.filter(number=number).exists():
            messages.info(request,'Cellphone has been used already.')
            return redirect('/register_hospital') 
         
        hospotalid = random_id(length=8,character_set=string.digits)
        autopassword_generator = random_id(length=7)
        create_new_hospital_account = User.objects.create_user(username=email,first_name=hospital_name,last_name=hospital_name,password=autopassword_generator,is_hospital=True,email=email,address=address,number=number,country=country,customerid=hospotalid,is_activation=True)
        if create_new_hospital_account:
            create_new_hospital_account.save()
            save_hospital_details=Hospital(hospital=create_new_hospital_account,hospitalid=hospotalid,package=package,desc=remarks)
            save_hospital_details.save()
            subject = 'Welcome to HMSS'
            from_email='HMS Software <no_reply@savemoregroup.com>'
            sento = email
            messagbody = '#'
            html_content =f'''<p><strong>Dear {hospital_name} </strong> <br><br>  This email serves to confirm that your Hospital Management account has been created successfully, 
            Login and starting placing orders at the confort of your sofas.
            <br> <strong>Login Credentials:</strong><br> 
            
            Username:{email} <br> Password: {autopassword_generator} <br><br> 
            
            Successful treatment starts with an accurate diagnosis, and our experts take the time to get it right. A team of specialists will listen to your needs and evaluate your condition from every angle to make the very best plan for you.            
            <br><hr> Best Regards <br> HMSS Software </p>'''
            msg=EmailMultiAlternatives(subject, messagbody, from_email,[sento])
            msg.attach_alternative(html_content, "text/html")
            Emailthread(msg).start()
            messages.info(request,'Account Created Successfully')
            return redirect('/register_hospital')  
        return render(request,'/register_hospital')
    else:
        return redirect('/register_hospital')  
    