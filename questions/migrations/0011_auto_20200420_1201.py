# Generated by Django 3.0.3 on 2020-04-20 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0001_initial'),
        ('questions', '0010_auto_20200420_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='language',
            field=models.CharField(default='Python', max_length=15),
        ),
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
            name='quid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_asker', to='signup.Signup'),
        ),
    ]