# Generated by Django 3.0.6 on 2020-05-09 23:35

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='profilepic',
            field=cloudinary.models.CloudinaryField(max_length=255),
        ),
    ]
