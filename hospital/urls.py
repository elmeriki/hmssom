from django.urls import path,include
from hospital import views

urlpatterns = [
    path('hospital_dashboard', views.hospital_dashboardView, name='hospital_dashboardView'),
    path('hospital_profile', views.hospital_profileView, name='hospital_profileView'),
    
    
    path('doctorsdashboard', views.doctorsdashboardView, name='doctorsdashboardView'),
    path('doctortreatment/<str:patientid>', views.doctortreatmentView, name='doctortreatmentView'),
    path('add_patient_test/<str:patientid>', views.add_patient_testView, name='add_patient_testView'),
    path('delete_patient_test/<str:patientid>/<str:test_id>', views.delete_patient_testView, name='delete_patient_testView'),

    path('create_treatment/<str:patientid>', views.create_treatmentView, name='create_treatmentView'),
    path('treatment_list', views.treatment_listView, name='treatment_listView'),
    path('patient_test_list/<str:patientid>', views.patient_test_listView, name='patient_test_listView'),


    path('compose_email', views.compose_emailView, name='compose_emailView'),
    path('send_bulk_email', views.send_bulk_emailView, name='send_bulk_emailView'),
    path('email_inbox', views.email_inboxView, name='email_inboxView'),


    path('department', views.departmentView, name='departmentView'),
    path('add_department', views.add_departmentView, name='add_departmentView'),
    path('save_add_department', views.save_add_departmentView, name='save_add_departmentView'),
    path('edit_department/<str:departmentid>', views.edit_departmentView, name='edit_departmentView'),
    path('update_department/<str:departmentid>', views.update_departmentView, name='update_departmentView'),
    path('delete_department/<str:departmentid>', views.delete_departmentView, name='delete_departmentView'),
    
    
    path('add_doctor', views.add_doctorView, name='add_doctorView'),
    path('doctor_list', views.doctor_listView, name='doctor_listView'),
    path('create_doctor', views.create_doctorView, name='create_doctorView'),
    path('edit_doctor/<str:doctorsid>', views.edit_doctorView, name='edit_doctorView'),
    path('update_doctor/<str:doctorsid>', views.update_doctorView, name='update_doctorView'),
    path('delete_doctor/<str:doctorsid>', views.delete_doctorView, name='delete_doctorView'),
    path('doctor_treatment_record', views.doctor_treatment_recordView, name='doctor_treatment_recordView'),
    path('doctor_visit', views.doctor_visitView, name='doctor_visitView'),
    path('add_doctor_visit', views.add_doctor_visitView, name='add_doctor_visitView'),


    
    path('add_patient', views.add_patientView, name='dd_patientView'),
    path('save_add_patient', views.save_add_patientView, name='save_add_patientiVew'),
    #path('create_patient', views.create_patientView, name='create_patientView'),
    path('patient_list', views.patient_listView, name='patient_listView'),
    path('edit_patient/<str:patientid>', views.edit_patientView, name='edit_patientView'),
    path('update_patient/<str:patientid>', views.update_patientView, name='update_patientView'),
    path('delete_patient/<str:patientid>', views.delete_patientView, name='delete_patientView'),
    path('patient_payments', views.patient_paymentsView, name='patient_paymentsView'),
    path('patient_payment_history', views.patient_payment_historyView, name='patient_payment_historyView'),
    path('case_list', views.case_listView, name='case_listView'),
    path('add_case', views.add_caseView, name='add_caseView'),
     path('document_list', views.document_listView, name='document_listView'),
    path('add_document', views.add_documentView, name='add_documentView'),



    path('add_humanresource', views.add_humanresourceView, name='add_humanresourceView'),
    path('create_humanresource', views.create_humanresourceView, name='create_humanresourceView'),
    path('humanresource_list', views.humanresource_listView, name='humanresource_listView'),
    path('humanresource_by_category/<str:category>', views.humanresource_by_categoryView, name='humanresource_by_categoryView'),
    path('edit_humanresource/<str:humanresourceid>', views.edit_humanresourceView, name='edit_humanresourceView'),
    path('update_humanresource/<str:humanresourceid>', views.update_humanresourceView, name='update_humanresourceView'),
    path('delete_humanresource/<str:humanresourceid>', views.delete_humanresourceView, name='delete_humanresourceView'),


    path('add_bedcategory', views.add_bedcategoryView, name='add_bedcategoryView'),
    path('create_bedcategory', views.create_bedcategoryView, name='create_bedcategoryView'),
    path('bedcategory_list', views.bedcategory_listView, name='bedcategory_listView'),


    path('add_childbirth', views.add_childbirthView, name='add_childbirthView'),
    path('create_childbirth', views.create_childbirthView, name='create_childbirthView'),
    path('childbirth_list', views.childbirth_listView, name='childbirth_listView'),


    path('add_deadthrecord', views.add_deadthrecordView, name='add_deadthrecordView'),
    path('create_deadthrecord', views.create_deadthrecordView, name='create_deadthrecordView'),
    path('deadthrecord_list', views.deadthrecord_listView, name='deadthrecord_listView'),


    path('add_donor', views.add_donorView, name='add_donorView'),
    path('create_donor', views.create_donorView, name='create_donorView'),
    path('donor_list', views.donor_listView, name='donor_listView'),


    path('add_file', views.add_fileView, name='add_fileView'),
    path('create_file', views.create_fileView, name='create_fileView'),
    path('file_list', views.file_listView, name='file_listView'),


    path('add_blood', views.add_bloodView, name='add_bloodView'),
    path('create_blood', views.create_bloodView, name='create_bloodView'),
    path('blood_list', views.blood_listView, name='blood_listView'),

   
    path('add_notice', views.add_noticeView, name='add_noticeView'),
    path('create_notice', views.create_noticeView, name='create_noticeView'),
    path('notice_list', views.notice_listView, name='notice_listView'),

    path('doctors_profile/<str:doctor_id>', views.doctors_profileView, name='doctors_profileView'),
    
    path('patient_details/<str:patient_id>', views.patient_detailsView, name='patient_detailsView'),

]


