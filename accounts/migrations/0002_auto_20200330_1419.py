# Generated by Django 3.0.3 on 2020-03-30 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_image.png', upload_to='profile_pics'),
        ),
    ]
