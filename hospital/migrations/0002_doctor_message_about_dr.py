# Generated by Django 3.2.19 on 2023-05-27 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='message_about_dr',
            field=models.TextField(blank=True, null=True),
        ),
    ]