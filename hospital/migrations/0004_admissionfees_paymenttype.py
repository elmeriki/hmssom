# Generated by Django 4.0.7 on 2023-08-09 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_admissionfees'),
    ]

    operations = [
        migrations.AddField(
            model_name='admissionfees',
            name='paymenttype',
            field=models.CharField(blank=True, default='None', max_length=200, null=True),
        ),
    ]