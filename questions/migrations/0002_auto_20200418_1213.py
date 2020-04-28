# Generated by Django 3.0.3 on 2020-04-18 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='question_to_answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_to_answer', to='questions.questions'),
        ),
    ]