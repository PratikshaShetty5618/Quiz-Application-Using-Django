# Generated by Django 2.1.7 on 2020-07-21 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0009_auto_20200721_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='easyquestionanwers',
            name='answer',
            field=models.CharField(blank=True, choices=[('1', 'Option 1'), ('2', 'Option 2'), ('3', 'Option 3'), ('4', 'Option 4'), ('5', 'Option 5')], default='', max_length=250),
        ),
    ]
