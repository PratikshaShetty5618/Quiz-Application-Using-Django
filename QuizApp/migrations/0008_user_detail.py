# Generated by Django 2.1.7 on 2020-07-11 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0007_delete_user_detail'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Do ensure to not make spelling mistakes as certificates cannot be reissued.', max_length=250, verbose_name='Name to be written on certificate')),
                ('email', models.EmailField(help_text='Do ensure to give proper email address without any errors.', max_length=250, verbose_name='Email Id where certificate could be sent')),
                ('attempted_at', models.DateTimeField(auto_now_add=True)),
                ('marks_obtained', models.SmallIntegerField(default=0, null=True)),
                ('status', models.CharField(choices=[('pass', 'Pass'), ('fail', 'Fail')], default='fail', max_length=250)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QuizApp.Quiz')),
            ],
        ),
    ]