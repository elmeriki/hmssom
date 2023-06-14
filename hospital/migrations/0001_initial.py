# Generated by Django 3.2.19 on 2023-06-14 05:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hospital_diff_departments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('phone', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('email', models.EmailField(blank=True, default='None', max_length=200, null=True)),
                ('address', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('password', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('departmentid', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('signature', models.ImageField(null=True, upload_to='doctors_signature/')),
                ('picture', models.ImageField(null=True, upload_to='doctors_pictures/')),
                ('profile', models.TextField(blank=True, null=True)),
                ('message_about_dr', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_department', to='hospital.department')),
                ('hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_belogs_to_hospital_names', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hospital_doctor_name', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('name', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('nok', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('non', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('phone', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('paymenttype', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_patient_is_admitted', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Paymentcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_category_name', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=11, null=True)),
                ('visitdsc', models.TextField(blank=True, null=True)),
                ('paymenttype', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('paymentstatus', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_category', to='hospital.paymentcategory')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_category_for_hospital', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_for_patient', to='hospital.patient')),
                ('treatedby_dr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_who_treated_patient', to='hospital.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Notices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('noticemsg', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_notice', to=settings.AUTH_USER_MODEL)),
                ('noticfor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_notice', to='hospital.department')),
            ],
        ),
        migrations.CreateModel(
            name='Leavetypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('duration', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_leave', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('reason', models.TextField(blank=True, default='N/A', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_leave_list', to=settings.AUTH_USER_MODEL)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_staffs', to=settings.AUTH_USER_MODEL)),
                ('typeofleave', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.leavetypes')),
            ],
        ),
        migrations.CreateModel(
            name='Labtest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testname', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=11, null=True)),
                ('paymenttype', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('reporttest', models.TextField(blank=True, default='N/A', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dr_lab_test', to=settings.AUTH_USER_MODEL)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hostital_lab_test', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_lab_test', to='hospital.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Humanresource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('title', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('name', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('email', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('address', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('phone', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('signature', models.ImageField(null=True, upload_to='employee_signature/')),
                ('picture', models.ImageField(null=True, upload_to='employee_pictures/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_human_resource', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospitalid', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('package', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_names', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('document', models.ImageField(null=True, upload_to='document/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_files', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expensescategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses_for_category', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decs', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=11, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses_for_categories', to='hospital.expensescategory')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses_for_hospital', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('type_sent', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_email', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('firstname', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('lastname', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('bloodgroup', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('weight', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('age', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('gender', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('phone', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('email', models.EmailField(blank=True, default='None', max_length=200, null=True)),
                ('lastdonationdate', models.DateField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_donor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('document', models.ImageField(null=True, upload_to='document/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_who_owns_document', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_document', to='hospital.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Deadthrecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('firstname', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('lastname', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('dod', models.DateField()),
                ('gender', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('race', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('address', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('desc', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('remark', models.TextField(blank=True, default='N/A', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_child_was_birthed', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Childbirth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('firstname', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('lastname', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('race', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('dob', models.DateField()),
                ('gender', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('weight', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('remark', models.TextField(blank=True, default='N/A', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_child_birth', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('messagesent', models.TextField(blank=True, default='N/A', null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('response', models.TextField(blank=True, default='N/A', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_to_hospital', to=settings.AUTH_USER_MODEL)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_to_staffs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Blood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bloodgroup', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('quantity', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_blood_grou', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bedcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryname', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('bednumber', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_bed_category', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
