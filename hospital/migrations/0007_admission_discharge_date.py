# Generated by Django 4.0.7 on 2023-08-09 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_remove_admission_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='admission',
            name='discharge_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
