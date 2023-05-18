# Generated by Django 4.0.7 on 2023-05-18 22:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital', '0005_remove_hospital_address_remove_hospital_country_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='pname',
            new_name='field',
        ),
        migrations.RenameField(
            model_name='doctor',
            old_name='qualification',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='Customer',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='desc',
        ),
        migrations.AddField(
            model_name='doctor',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_department', to='hospital.department'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='picture',
            field=models.ImageField(null=True, upload_to='doctors_pictures/'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='signature',
            field=models.ImageField(null=True, upload_to='doctors_signature/'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hospital_doctor_name', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_belogs_to_hospital_names', to=settings.AUTH_USER_MODEL),
        ),
    ]
