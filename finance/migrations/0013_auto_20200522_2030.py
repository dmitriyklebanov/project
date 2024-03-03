# Generated by Django 3.0.6 on 2020-05-22 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0012_transfer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='currency',
            field=models.CharField(choices=[('USD', 'United States Dollar'), ('EUR', 'Euro'), ('RUS', 'Russian Ruble')], default='USD', max_length=5),
        ),
    ]
