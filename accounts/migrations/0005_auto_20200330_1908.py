# Generated by Django 3.0.3 on 2020-03-30 19:08

from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200330_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=phone_field.models.PhoneField(blank=True, max_length=31),
        ),
    ]
