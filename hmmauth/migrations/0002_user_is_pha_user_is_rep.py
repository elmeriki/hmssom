# Generated by Django 4.0.7 on 2023-06-23 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hmmauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_pha',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_rep',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]