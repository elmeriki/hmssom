# Generated by Django 4.0.7 on 2023-06-19 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='region',
            options={'verbose_name_plural': 'Region List'},
        ),
        migrations.AddField(
            model_name='region',
            name='color',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
    ]
