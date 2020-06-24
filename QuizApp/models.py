from django.db import models
import datetime

from django.core.validators import (
    MaxValueValidator, validate_comma_separated_integer_list,
)
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import User

# Create your models here.


# class CategoryManager(models.Manager):

#     def new_category(self, category):
#         new_category = self.create(category=re.sub('\s+', '-', category)
#                                    .lower())
#         new_category.save()
#         return new_category

class Category(models.Model):

    category = models.CharField(
        verbose_name=("Category"),
        max_length=250, blank=True,
        unique=True, null=True)

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.category

class Quiz(models.Model):
    MARKING_CHOICES = [
    ('same', 'Same Marking for all Category'),
    ('different', 'Different Marking for all Category'),
    ]

    title = models.CharField(
        verbose_name=("Title"),
        max_length=60, blank=False)

    description = models.TextField(
        verbose_name=("Description"),
        default = "Get Set Go",
        blank=True, help_text=("A description of the quiz. [Optional]"))

    category = models.ForeignKey(
        Category, null=True, blank=True,
        verbose_name=("Category"), on_delete=models.CASCADE)

    random_order = models.BooleanField(
        blank=False, default=False,
        verbose_name=("Random Order"),
        help_text=("Display the questions in "
                    "a random order or as they "
                    "are set?"))

    max_questions = models.PositiveIntegerField(
        blank=True, null=True, verbose_name=("Max Questions"),
        help_text=("Number of questions to be asked on each attempt. [Optional]"))

    answers_at_end = models.BooleanField(
        blank=False, default=False,
        help_text=("Correct answer is NOT shown after question."
                    " Answers displayed at the end."),
        verbose_name=("Answers at end"))

    pass_mark = models.SmallIntegerField(
        blank=False, default=100,
        verbose_name=("Pass Mark"),
        help_text=("Percentage required to pass exam."),
        validators=[MaxValueValidator(100)])

    marking = models.CharField(max_length=250, choices=MARKING_CHOICES, default='same')

    success_text = models.TextField(
        blank=True, help_text=("Displayed if user passes. [Optional]"),
        verbose_name=("Success Text"))

    fail_text = models.TextField(
        verbose_name=("Fail Text"),
        blank=True, help_text=("Displayed if user fails. [Optional]"))

    time_alloted = models.CharField(
        max_length=250,
        verbose_name=("Time Alloted"),
        blank=False, help_text=("Time to be alloted for Quiz."),)

    # time_alloted = models.TextField()

    slug = models.SlugField(max_length = 250, null = True, blank = True,)

    quiz_setter = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    

    def save(self, force_insert=False, force_update=False, *args, **kwargs):

        if self.pass_mark > 100:
            raise ValidationError('%s is above 100' % self.pass_mark)

        super(Quiz, self).save(force_insert, force_update, *args, **kwargs)

    class Meta:
        verbose_name = ("Quiz")
        verbose_name_plural = ("Quizzes")

    def __str__(self):
        return self.title

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=get_random_string(length=6)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Quiz)

class Same_Marking(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    marks = models.SmallIntegerField(
        blank=False, default=100,
        verbose_name=("Marks"),
        help_text=("Marks to be alloted on right answer."),
        validators=[MaxValueValidator(100)])
    neg = models.SmallIntegerField(
        blank=False, default=0,
        verbose_name=("Negative Marking"),
        help_text=("Marks to be deducted on wrong answer. If no negative marking is to be opted then enter 0."),
        validators=[MaxValueValidator(100)])

    def save(self, force_insert=False, force_update=False, *args, **kwargs):

        if self.marks > 100 or self.neg > 100:
            raise ValidationError("Marks entered is inappropriate")

        super(Quiz, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return self.quiz

class Different_Marking(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    easy_marks = models.SmallIntegerField(
        blank=False, default=100,
        verbose_name=("Marks for Easy Questions"),
        help_text=("Marks to be alloted on right answer."),
        validators=[MaxValueValidator(100)])
    easy_neg = models.SmallIntegerField(
        blank=False, default=0,
        verbose_name=("Negative Marking for Easy Questions"),
        help_text=("Marks to be deducted on wrong answer. If no negative marking is opted then enter 0."),
        validators=[MaxValueValidator(100)])
    medium_marks = models.SmallIntegerField(
        blank=False, default=100,
        verbose_name=("Marks for Medium Questions"),
        help_text=("Marks to be alloted on right answer."),
        validators=[MaxValueValidator(100)])
    medium_neg = models.SmallIntegerField(
        blank=False, default=0,
        verbose_name=("Negative Marking for Medium Questions"),
        help_text=("Marks to be deducted on wrong answer. If no negative marking is opted then enter 0."),
        validators=[MaxValueValidator(100)])
    hard_marks = models.SmallIntegerField(
        blank=False, default=100,
        verbose_name=("Marks for Hard Questions"),
        help_text=("Marks to be alloted on right answer."),
        validators=[MaxValueValidator(100)])
    hard_neg = models.SmallIntegerField(
        blank=False, default=0,
        verbose_name=("Negative Marking for Hard Questions"),
        help_text=("Marks to be deducted on wrong answer. If no negative marking is opted then enter 0."),
        validators=[MaxValueValidator(100)])

    def save(self, force_insert=False, force_update=False, *args, **kwargs):

        if self.easy_marks > 100 or self.easy_neg > 100 or self.medium_marks > 100 or self.medium_neg > 100 or self.hard_marks > 100 or self.hard_neg > 100:
            raise ValidationError("Marks entered is inappropriate")

    def __str__(self):
        return self.quiz