# Generated by Django 4.2.10 on 2024-03-03 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20200520_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default/profile_image.jpg', upload_to='profile_pics'),
        ),
    ]