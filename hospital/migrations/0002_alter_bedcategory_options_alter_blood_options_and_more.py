# Generated by Django 4.0.7 on 2023-06-19 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bedcategory',
            options={'verbose_name_plural': 'Bedcategory'},
        ),
        migrations.AlterModelOptions(
            name='blood',
            options={'verbose_name_plural': 'Blood'},
        ),
        migrations.AlterModelOptions(
            name='chat',
            options={'verbose_name_plural': 'Chat'},
        ),
        migrations.AlterModelOptions(
            name='childbirth',
            options={'verbose_name_plural': 'Childbirth'},
        ),
        migrations.AlterModelOptions(
            name='deadthrecord',
            options={'verbose_name_plural': 'Deadthrecord'},
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name_plural': 'Department'},
        ),
        migrations.AlterModelOptions(
            name='doctor',
            options={'verbose_name_plural': 'Doctor'},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name_plural': 'Document'},
        ),
        migrations.AlterModelOptions(
            name='donor',
            options={'verbose_name_plural': 'Donor'},
        ),
        migrations.AlterModelOptions(
            name='email',
            options={'verbose_name_plural': 'Email'},
        ),
        migrations.AlterModelOptions(
            name='expense',
            options={'verbose_name_plural': 'Expense'},
        ),
        migrations.AlterModelOptions(
            name='expensescategory',
            options={'verbose_name_plural': 'Expensescategory'},
        ),
        migrations.AlterModelOptions(
            name='file',
            options={'verbose_name_plural': 'File'},
        ),
        migrations.AlterModelOptions(
            name='hospital',
            options={'verbose_name_plural': 'Hospital'},
        ),
        migrations.AlterModelOptions(
            name='humanresource',
            options={'verbose_name_plural': 'Humanresource'},
        ),
        migrations.AlterModelOptions(
            name='labresult',
            options={'verbose_name_plural': 'Labresult'},
        ),
        migrations.AlterModelOptions(
            name='labtest',
            options={'verbose_name_plural': 'Labtest'},
        ),
        migrations.AlterModelOptions(
            name='lapreport',
            options={'verbose_name_plural': 'Lapreport'},
        ),
        migrations.AlterModelOptions(
            name='leave',
            options={'verbose_name_plural': 'Leave'},
        ),
        migrations.AlterModelOptions(
            name='leavetypes',
            options={'verbose_name_plural': 'Leavetypes'},
        ),
        migrations.AlterModelOptions(
            name='notices',
            options={'verbose_name_plural': 'Notices'},
        ),
        migrations.AlterModelOptions(
            name='patient',
            options={'verbose_name_plural': 'Patient'},
        ),
        migrations.AlterModelOptions(
            name='patienttest',
            options={'verbose_name_plural': 'Patienttest'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name_plural': 'Payment'},
        ),
        migrations.AlterModelOptions(
            name='paymentcategory',
            options={'verbose_name_plural': 'Paymentcategory'},
        ),
        migrations.AlterModelOptions(
            name='treatment',
            options={'verbose_name_plural': 'Treatment'},
        ),
    ]
