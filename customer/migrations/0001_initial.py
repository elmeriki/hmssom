# Generated by Django 4.0.7 on 2023-06-21 12:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hospital', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('note', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('advice', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('date', models.DateField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hospital_dr_gives_prescription', to='hospital.doctor')),
                ('hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hospital_dr_patient_prescription', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_patient_receives_prescription', to='hospital.patient')),
            ],
            options={
                'verbose_name_plural': 'Prescription',
            },
        ),
        migrations.CreateModel(
            name='Medicinecategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryname', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('desc', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_medicine_for_category', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Medicinecategory',
            },
        ),
        migrations.CreateModel(
            name='Medicinal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('storebox', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('purchaseprice', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=11, null=True)),
                ('saleprice', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=11, null=True)),
                ('quantity', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('genericname', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('company', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('effects', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('expiredate', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_medicine_for_category', to='customer.medicinecategory')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_medicine', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Medicinal',
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitdsc', models.TextField(blank=True, null=True)),
                ('remark', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('astatus', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=11, null=True)),
                ('date', models.DateField(blank=True, default=0, null=True)),
                ('paymenttype', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('paymentstatus', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dr_who_is_alocated', to='hospital.doctor')),
                ('hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hospital_appointment_name', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_appointment_name', to='hospital.patient')),
            ],
            options={
                'verbose_name_plural': 'Appoint List',
            },
        ),
    ]
