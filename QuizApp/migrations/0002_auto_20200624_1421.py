# Generated by Django 2.1.7 on 2020-06-24 08:51

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('QuizApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='marking',
            field=models.CharField(choices=[('same', 'Same Marking for all Category'), ('different', 'Different Marking for all Category')], default='same', max_length=250),
        ),
        migrations.AddField(
            model_name='quiz',
            name='quiz_setter',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='time_alloted',
            field=models.CharField(help_text='Time to be alloted for Quiz.', max_length=250, verbose_name='Time Alloted'),
        ),
        migrations.AlterField(
            model_name='same_marking',
            name='neg',
            field=models.SmallIntegerField(default=0, help_text='Marks to be deducted on wrong answer. If no negative marking is to be opted then enter 0.', validators=[django.core.validators.MaxValueValidator(100)], verbose_name='Negative Marking'),
        ),
    ]