# Generated by Django 5.0 on 2024-09-03 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careerapp', '0003_jobseeker_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruiter',
            name='location',
            field=models.CharField(max_length=22225, null=True),
        ),
    ]
