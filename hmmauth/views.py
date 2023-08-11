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
from hospital.models import *
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
        
        
        
@login_required(login_url='/')  
def superadminView(request):
    if request.user.is_authenticated and request.user.is_superuser:
        data = {
            'general_hospital_appointment':Appointment.objects.all().count(),
            'total_hospital_count':User.objects.filter(is_hospital=True).count(),
            'total_user_count':User.objects.all().count(),
            'total_doctor_count':User.objects.filter(is_dr=True).count(),
            'active_hospital_list':User.objects.filter(is_hospital=True,is_activation=True),
        }
        return render(request,'superadmin/index.html',context=data)
    
def welcomeView(request):
    return render(request,'web/index.html',context={})

def contactView(request):
    return render(request,'web/contact.html',context={})

def password_recoveryView(request):
    return render(request,'hospital/password_recovery.html',context={})

def password_recovery_View(request):
    if request.method=="POST":
        email = request.POST['email']
        if not User.objects.filter(username=email).exists():
           messages.info(request,"Email Address is not recognised") 
           return redirect('/password_recovery')
       
        hospital_instance=User.objects.get(username=email)
        if not Passcode.objects.filter(hospital=hospital_instance).exists():
           messages.info(request,"Password recovery could not be completed") 
           return redirect('/password_recovery')
         
        if User.objects.filter(username=email).exists():
            passcord_recovery_instance=Passcode.objects.get(hospital=hospital_instance)
            subject='HMSS Password Recovery'
            from_email='HMS Software <no_reply@savemoregroup.com>'
            sento=email
            messagbody = '#'
            html_content =f'''<p><strong>Dear {hospital_instance.first_name} </strong> <br><br>  If you did not ask to recovery your password you may want to review your recent account access for any unusual activity.<br> 
            We're here to help if you need it. Visit the Help Center for more info or contact us.
            <br> <strong>Login Credentials:</strong><br> 
            Username:{email} <br> Password:{passcord_recovery_instance.password} <br><br> 
        
            It Tech Solutions Company will provide you the best & highly accurate analysis that will let you make reliable decisions related to your Hospital.            
            <br><hr> Best Regards <br> HMSS Software </p>'''
            msg=EmailMultiAlternatives(subject, messagbody, from_email,[sento])
            msg.attach_alternative(html_content, "text/html")
            Emailthread(msg).start()
            messages.info(request,'Password recovery has been completed. Please check your email for confirmation.')
            return redirect('/password_recovery')
    else:
        return redirect('/')
    
def sysView(request):
    return render(request,'hospital/login.html',context={})


def hospital_loginView(request):
    return render(request,'hospital/login.html')
    

def register_loginView(request):
    data = {
     'list_of_regions':Region.objects.filter(status=0),
     'list_currency':Curency.objects.all()
    }
    return render(request,'hospital/register.html',context=data)

def logoutView(request):
    auth.logout(request)
    messages.info(request,"Logout Successfully")
    return redirect('/sys') 


def hospital_login_View(request):
    if request.method =="POST" and request.POST['username'] and request.POST['password']:
        username = request.POST['username']
        password =request.POST['password']
        
        userlog = auth.authenticate(username=username,password=password)
        # checking if it is an existing user in the database
        
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and not request.user.is_activation:
                messages.info(request,"Account is not active or suspended")
                return redirect('/sys')
                
        if not User.objects.filter(username=username).exists():
            messages.info(request,'Incorrect login credentials.')
            return redirect('/sys')  
        
        
        # customise error messages handler
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_hospital and request.user.is_paid:
                return redirect('/hospital_dashboard')
            
            if request.user.is_authenticated and request.user.is_hospital and not request.user.is_paid:
                messages.info(request,"Your account is suspended for none payment of your licence fees")
                return redirect('/sys')
        else:
            messages.info(request,"Incorrect login credentials")
            return redirect('/sys')
                
            
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_dr:
                return redirect('/doctorsdashboard')
        else:
            messages.info(request,"Incorrect login credentials.")
            return redirect('/sys')
        
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_superuser:
                return redirect('/superadmin')
        else:
            messages.info(request,"Incorrect login credentials.")
            return redirect('/sys')
        
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_lab:
                return redirect('/labdashboard')
        else:
            messages.info(request,"Incorrect login credentials.")
            return redirect('/sys')
        
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_rep:
                return redirect('/recepdashboard')
        else:
            messages.info(request,"Incorrect login credentials.")
            return redirect('/sys')
        
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_pha:
                return redirect('/phamardashboard')
        else:
            messages.info(request,"Incorrect login credentials.")
            return redirect('/sys')
            
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_customer:
                return redirect('/sys')
        else:
            messages.info(request,"Incorrect login credentials.")
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
        region = request.POST['country']
        currency = request.POST['currency']
        autopassword_generator = request.POST['password']
        if len(request.FILES) != 0:
            logo=request.FILES['logo']
            logofilesize=logo.size
            if logofilesize > 2621440:
                messages.info(request,"Your Logo is Biger Than 2MB")
                return redirect('/register_hospital')
        
        if User.objects.filter(email=email).exists():
            messages.info(request,'Email has been used already.')
            return redirect('/register_hospital')  
        
        if User.objects.filter(number=number).exists():
            messages.info(request,'Cellphone has been used already.')
            return redirect('/register_hospital') 
         
        hospotalid = random_id(length=8,character_set=string.digits)
        create_new_hospital_account = User.objects.create_user(username=email,first_name=hospital_name,last_name=hospital_name,password=autopassword_generator,is_hospital=True,email=email,address=address,number=number,city=region,customerid=hospotalid,is_activation=False,currency=currency,logo=logo)
        if create_new_hospital_account:
            create_new_hospital_account.save()
            save_hospital_details=Hospital(hospital=create_new_hospital_account,hospitalid=hospotalid,package=package,desc=remarks)
            save_hospital_details.save()
            save_pass_code =Passcode(hospital=create_new_hospital_account,password=autopassword_generator)
            save_pass_code.save()
            subject = 'Welcome to HMSS'
            from_email='HMS Software <no_reply@savemoregroup.com>'
            sento = email
            messagbody = '#'
            html_content =f'''<p><strong>Dear {hospital_name} </strong> <br><br>  This email serves to confirm that your Hospital Management account has been created successfully, 
            Contact system administrator for payment and account activations.
            <br> <strong>Login Credentials:</strong><br> 
            
            Username:{email} <br> Password: {autopassword_generator} <br><br> 
            
            It Tech Solutions Company will provide you the best & highly accurate analysis that will let you make reliable decisions related to your Hospital.            
            <br><hr> Best Regards <br> HMSS Software </p>'''
            msg=EmailMultiAlternatives(subject, messagbody, from_email,[sento])
            msg.attach_alternative(html_content, "text/html")
            Emailthread(msg).start()
            messages.info(request,'Account Created Successfully')
            return redirect('/register_hospital')  
        return render(request,'/register_hospital')
    else:
        return redirect('/register_hospital')  
    
def password_updateView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        email_address = request.POST['email']
        new_password = request.POST['new_password'] 
        hospital_instance=User.objects.get(username=email_address)
        hospital_instance.set_password(new_password)
        hospital_instance.save()
        auth.logout(request)
        messages.info(request,"Password changed Successfully")
        return redirect('/sys') 