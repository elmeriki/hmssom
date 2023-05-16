# Generated by Django 3.2.18 on 2023-05-16 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='humanresource',
            old_name='adress',
            new_name='address',
        ),
        migrations.AlterField(
            model_name='deadthrecord',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_child_was_birthed', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='deadthrecord',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_who_died', to='hospital.patient'),
        ),
        migrations.AlterField(
            model_name='labtest',
            name='dr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dr_lab_test', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='leave',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_leave_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='leavetypes',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_leave', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='patient',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_patient_is_admitted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('desc', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_diff_departments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='humanresource',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='human_resource_categories', to='hospital.department'),
        ),
        migrations.AlterField(
            model_name='notice',
            name='noticfor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_notice', to='hospital.department'),
        ),
        migrations.DeleteModel(
            name='Departments',
        ),
    ]
