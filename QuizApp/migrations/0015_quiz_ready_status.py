# Generated by Django 2.1.7 on 2020-07-23 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0014_auto_20200723_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='ready_status',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
