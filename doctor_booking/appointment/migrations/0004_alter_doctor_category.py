# Generated by Django 5.1.1 on 2024-09-22 04:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_alter_doctor_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appointment.category'),
        ),
    ]
