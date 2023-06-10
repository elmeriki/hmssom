# Generated by Django 3.2.19 on 2023-06-07 02:39

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
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('category', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('storebox', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('purchaseprice', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=11, null=True)),
                ('saleprice', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=11, null=True)),
                ('quantity', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('genericname', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('company', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('effects', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('expiredate', models.DateField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hostital_medicine', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history', models.TextField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('advice', models.TextField(blank=True, null=True)),
                ('date', models.DateField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_dr_gives_prescription', to=settings.AUTH_USER_MODEL)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_dr_patient_prescription', to=settings.AUTH_USER_MODEL)),
                ('medicine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_department', to='customer.medicine')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_patient_receives_prescription', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitdsc', models.TextField(blank=True, null=True)),
                ('remark', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=11, null=True)),
                ('date', models.DateField(auto_now=True)),
                ('paymenttype', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('paymentstatus', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dr_who_is_alocated', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_appointment_name', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
