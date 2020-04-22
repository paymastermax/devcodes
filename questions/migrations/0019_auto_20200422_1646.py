# Generated by Django 3.0.5 on 2020-04-22 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0001_initial'),
        ('questions', '0018_auto_20200422_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='auid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_answerer', to='signup.Signup'),
        ),
        migrations.AlterField(
            model_name='answers',
            name='question_to_answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_to_answer', to='questions.Questions'),
        ),
        migrations.AlterField(
            model_name='questions',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to='signup.Signup'),
        ),
        migrations.AlterField(
            model_name='questions',
            name='quid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_asker', to='signup.Signup'),
        ),
    ]
