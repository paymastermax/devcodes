# Generated by Django 3.0.5 on 2020-05-07 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
