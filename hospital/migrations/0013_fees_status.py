# Generated by Django 4.0.7 on 2023-07-06 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0012_remove_fees_created_at_remove_fees_dayscount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fees',
            name='status',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
    ]
