# Generated by Django 4.0.7 on 2023-06-28 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hmmauth', '0003_user_is_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hospital_id',
            field=models.CharField(blank=True, default='None', max_length=200, null=True),
        ),
    ]
