# Generated by Django 4.0.7 on 2023-06-10 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_doctor_departmentid'),
        ('customer', '0003_appointment_hospital_alter_appointment_dr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='dr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dr_who_is_alocated', to='hospital.doctor'),
        ),
    ]
