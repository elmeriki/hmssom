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


class Emailthread(threading.Thread):
    def __init__(self,msg):
        self.msg=msg
        threading.Thread.__init__(self)
    def run(self):
        self.msg.send(fail_silently=False)

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
def hospital_profileView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        about_the_hospital_text=Hospital.objects.get(hospital=hospital_instance)
        data = {
        'count_number_of_patient':Patient.objects.filter(hospital=hospital_instance).count(),
        'count_number_of_doctors':Doctor.objects.filter(hospital=hospital_instance).count(),
        'about_the_hospital_text':about_the_hospital_text.desc
        }
        return render(request,'hospital/profile.html',context=data)

@login_required(login_url='/')  
def compose_emailView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        sent_email_count = Email.objects.filter(hospital=hospital_instance).count()
        data = {
            'sent_email_count':sent_email_count
        }
        return render(request,'hospital/compose.html',context=data)
    
@login_required(login_url='/')  
def email_inboxView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        sent_email_count = Email.objects.filter(hospital=hospital_instance).count()
        data = {
            'sent_email_count':sent_email_count
        }
        return render(request,'hospital/inbox.html',context=data)

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def send_bulk_emailView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        category = request.POST['category']
        title = request.POST['title']
        message = request.POST['text']
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        if category == "All":
            if not Humanresource.objects.filter(hospital=hospital_instance):
                messages.info(request,'No Email Found')
                return redirect('/compose_email')
            if Humanresource.objects.filter(hospital=hospital_instance):
                fetch_all_staff_email=Humanresource.objects.filter(hospital=hospital_instance)
                for each_staff_info in fetch_all_staff_email:
                    subject=title
                    from_email=f'{each_staff_info.hospital.first_name} <no_reply@savemoregroup.com>'
                    sento = each_staff_info.email
                    messagbody = '#'
                    html_content =f'''<p><strong>Dear {each_staff_info.name} </strong> <br><br>  
                    {message}
                    <br><hr> Best Regards <br> {each_staff_info.hospital.first_name} </p>'''
                    msg=EmailMultiAlternatives(subject, messagbody, from_email,[sento])
                    msg.attach_alternative(html_content, "text/html")
                    Emailthread(msg).start()
            save_sent_email=Email(hospital=hospital_instance,title=title,message=message)
            if save_sent_email:
                save_sent_email.save()
                messages.info(request,'Email sent successfully to all staffs') 
                return redirect('/compose_email')
        else:
            messages.info(request,'Something went wrong while sending email') 
            return redirect('/compose_email')
        
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
        category = request.POST['category']
        title = request.POST['title']
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        number = request.POST['phone']        
        id = random_id(length=10,character_set=string.digits)
    
        save_humanresource_details=Humanresource(hospital=hospital_instance, id=id,category=category,title=title,name=name,email=email,address=address,phone=number,signature=signature,picture=picture)
        save_humanresource_details.save()
        messages.info(request,'Employee Profile created successfully')
        return redirect('/add_humanresource')

   
@login_required(login_url='/')  
def add_humanresourceView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        return render(request,'hospital/add_humanresource.html')
    
    
def humanresource_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        list_all_humanresource=Humanresource.objects.filter(hospital=hospital_instance)
        hr_data = {
            'list_all_humanresource':list_all_humanresource 
        }
        return render(request,'hospital/humanresource_list.html',context=hr_data)
    
def humanresource_by_categoryView(request,category):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        if category == "Doctor":
            list_all_doctor=Humanresource.objects.filter(hospital=hospital_instance,category=category)
            data = {
                'list_all_doctor':list_all_doctor
            }
            return render(request,'hospital/humanresource_list.html',context=data)
        if category == "Nurse":
            list_all_nurses=Humanresource.objects.filter(hospital=hospital_instance,category=category)
            data = {
                'list_all_nurses':list_all_nurses
            }
            return render(request,'hospital/humanresource_list.html',context=data)
        
        if category == "Phamarcist":
            list_all_phamarcist=Humanresource.objects.filter(hospital=hospital_instance,category=category)
            data = {
                'list_all_phamarcist':list_all_phamarcist
            }
            return render(request,'hospital/humanresource_list.html',context=data)
        if category == "Laboratorist":
            list_all_laboratorist=Humanresource.objects.filter(hospital=hospital_instance,category=category)
            data = {
                'list_all_laboratorist':list_all_laboratorist
            }
            return render(request,'hospital/humanresource_list.html',context=data)
        
        if category == "Accountant":
            list_all_accountant=Humanresource.objects.filter(hospital=hospital_instance,category=category)
            data = {
                'list_all_accountant':list_all_accountant
            }
            return render(request,'hospital/humanresource_list.html',context=data)
        
        if category == "Receptionist":
            list_all_receptionist=Humanresource.objects.filter(hospital=hospital_instance,category=category)
            data = {
                'list_all_receptionist':list_all_receptionist
            }
            return render(request,'hospital/humanresource_list.html',context=data)
        
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_appointmentView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
        return render(request,'hospital/add_appointment.html',{})
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_appointmentView(request):
    #if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
    return render(request,'hospital/add_appointment.html')

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def appointment_listView(request):
    #if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":        
    return render(request,'hospital/appointment_list.html')
    

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_bedcategoryView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        return render(request,'hospital/add_bedcategory.html')

    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_bedcategoryView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        categoryname = request.POST['categoryname']
        bednumber = request.POST['bednumber']
        status = request.POST['status']       
        id = random_id(length=9,character_set=string.digits)
    
        save_bedcategory_details=Bedcategory(hospital=hospital_instance, id=id, categoryname=categoryname,bednumber=bednumber,status=status)
        save_bedcategory_details.save()
        messages.info(request,'Bed Category created successfully')
        return redirect('/add_bedcategory')
      

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def bedcategory_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        list_all_bedcategories=Bedcategory.objects.filter(hospital=hospital_instance)
        bedcategory_data = {
            'list_all_bedcategories':list_all_bedcategories
        }
        return render(request,'hospital/bedcategory_list.html',context=bedcategory_data)
    
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_childbirthView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        title = request.POST['title']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        dob = request.POST['dob'] 
        gender = request.POST['gender']  
        weight = request.POST['weight']
        race = request.POST['race']
        remark = request.POST['remark']
             
        id = random_id(length=9,character_set=string.digits)
    
        save_childbirth_details=Childbirth(hospital=hospital_instance, id=id, title=title,firstname=firstname, lastname=lastname,
                                            dob=dob, gender=gender,weight=weight, race=race, remark=remark)
        save_childbirth_details.save()
                                             
        messages.info(request,'Child birth record created successfully')
        return redirect('/add_childbirth')
    
       
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_childbirthView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        return render(request,'hospital/add_childbirth.html')


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def childbirth_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        list_all_childbirth=Childbirth.objects.filter(hospital=hospital_instance)
        childbirth_data = {
            'list_all_childbirth':list_all_childbirth
        }
        return render(request,'hospital/childbirth_list.html',context=childbirth_data)
       

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_deadthrecordView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        title = request.POST['title']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        dod = request.POST['dod'] 
        gender = request.POST['gender']  
        phone = request.POST['phone']
        address = request.POST['address']
        desc = request.POST['desc']
        race = request.POST['race']
        remark = request.POST['remark']
             
        id = random_id(length=9,character_set=string.digits)
    
        save_deadthrecord_details=Deadthrecord(hospital=hospital_instance, id=id, title=title,firstname=firstname, lastname=lastname,
                                            dod=dod, gender=gender,phone=phone, address=address,desc=desc, race=race, remark=remark)
        save_deadthrecord_details.save()
                                             
        messages.info(request,'Death record created successfully')
        return redirect('/add_deadthrecord')
    
       
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_deadthrecordView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        return render(request,'hospital/add_deathrecord.html')


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def deadthrecord_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        list_all_deadthrecord=Deadthrecord.objects.filter(hospital=hospital_instance)
        deadthrecord_data = {
            'list_all_deadthrecord':list_all_deadthrecord
        }
        return render(request,'hospital/deathrecord_list.html',context=deadthrecord_data)

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_donorView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        title = request.POST['title']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        bloodgroup = request.POST['bloodgroup'] 
        weight = request.POST['weight']
        age = request.POST['age']
        gender = request.POST['gender']  
        phone = request.POST['phone']
        email = request.POST['email']       
        id = random_id(length=9,character_set=string.digits)
    
        save_donor_details=Donor(hospital=hospital_instance, id=id, title=title, firstname=firstname, lastname=lastname, bloodgroup=bloodgroup, weight=weight, age=age, gender=gender,phone=phone, email=email)
        save_donor_details.save()
                                             
        messages.info(request,'Donor created successfully')
        return redirect('/add_donor')
    
       
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_donorView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        return render(request,'hospital/add_donor.html')


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def donor_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        all_donor_list=Donor.objects.filter(hospital=hospital_instance)
        donor_data = {
            'all_donor_list':all_donor_list
        }
        return render(request,'hospital/donor_list.html',context=donor_data)
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def create_fileView(request):
    if request.user.is_authenticated and request.user.is_hospital and request.method=="POST":
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        if len(request.FILES) != 0:
            document=request.FILES['document']
            documentfilesize=document.size
            if documentfilesize > 2621440  > 2621440:
                messages.info(request,"The File is Biger Than 2MB")
                return redirect('/add_file')
        title = request.POST['title']
            
        id = random_id(length=9,character_set=string.digits)
    
        save_file_details=File(hospital=hospital_instance, id=id, title=title, document=document)
        save_file_details.save()
                                             
        messages.info(request,'File created successfully')
        return redirect('/add_file')
    
       
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_fileView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        return render(request,'hospital/add_file.html')


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def file_listView(request):
    if request.user.is_authenticated and request.user.is_hospital:
        username=request.user.username
        hospital_instance=User.objects.get(username=username)
        all_file_list=File.objects.filter(hospital=hospital_instance)
        file_data = {
            'all_file_list':all_file_list
        }
        return render(request,'hospital/file_list.html',context=file_data)

