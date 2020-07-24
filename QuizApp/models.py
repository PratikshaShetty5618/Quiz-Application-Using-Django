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
        Category, null=True, blank=False,
        verbose_name=("Category"), on_delete=models.CASCADE)

    random_order = models.BooleanField(
        blank=False, default=False,
        verbose_name=("Random Order"),
        help_text=("Display the questions in "
                    "a random order or as they "
                    "are set?"))

    max_questions = models.PositiveIntegerField(
        blank=False, null=True, verbose_name=("Max Questions"),
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
        verbose_name=("Success Text"), default = "Hey, you successfully passed the quiz. It was difficult but you indeed succeeded. Congratulations and wish you more success!!!.")

    fail_text = models.TextField(
        verbose_name=("Fail Text"),
        blank=True, help_text=("Displayed if user fails. [Optional]"), default = "Hey, you were not able to pass this time. But don't lose hope. Work hard and come with a bang next time.")

    time_alloted = models.CharField(
        max_length=250,
        verbose_name=("Time Alloted"),
        blank=False, help_text=("Time to be alloted for Quiz."),)

    # # time_alloted = models.DurationField(
    #     verbose_name=("Time Alloted"),
    #     blank=False, help_text=("Time to be alloted for Quiz."),)
    # time_alloted = models.TextField()

    slug = models.SlugField(max_length = 250, null = True, blank = True,)

    quiz_setter = models.ForeignKey(User,on_delete=models.CASCADE,default=None)

    ready_status = models.BooleanField(blank=True, default=False)
    

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

class EasyQuestionAnwers(models.Model):
    TYPE_CHOICES = [
    ('single', 'Single Correct Answer'),
    ('multiple', 'Multiple Correct Answers'),
    ]
    ANSWER_CHOICES = [
    ('1', 'Option 1'),
    ('2', 'Option 2'),
    ('3', 'Option 3'),
    ('4', 'Option 4'),
    ('5', 'Option 5'),
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    type_of_quiz = models.CharField(max_length=250, choices=TYPE_CHOICES, default='single')
    question = models.TextField(
        verbose_name=("Question"),
        blank=False)
    option_1 = models.TextField(
        verbose_name=("Type Option 1"),
        help_text=("Enetr option 1. This field has to be filled compulsorily."),
        blank=False)
    option_2 = models.TextField(
        verbose_name=("Type Option 2"),
        help_text=("Enter option 2. This field has to be filled compulsorily."),
        blank=True)
    option_3 = models.TextField(
        verbose_name=("Type Option 3"),
        help_text=("Enter option 3. If not required, then skip and leave the field blank."),
        default="",
        blank=True)
    option_4 = models.TextField(
        verbose_name=("Type Option 4"),
        help_text=("Enter option 4. If not required, then skip and leave the field blank."),
        default="",
        blank=True)
    option_5 = models.TextField(
        verbose_name=("Type Option 5"),
        help_text=("Enter option 5. If not required, then skip and leave the field blank."),
        default="",
        blank=True)
    answer = models.CharField(max_length=250, choices=ANSWER_CHOICES,  blank=True)
    answers = models.CharField(max_length=250, default="")
    level = models.CharField(max_length=250, null=False, blank=False, default="easy")

    def __str__(self):
        return self.question

class MediumQuestionAnwers(models.Model):
    TYPE_CHOICES = [
    ('single', 'Single Correct Answer'),
    ('multiple', 'Multiple Correct Answers'),
    ]
    ANSWER_CHOICES = [
    ('1', 'Option 1'),
    ('2', 'Option 2'),
    ('3', 'Option 3'),
    ('4', 'Option 4'),
    ('5', 'Option 5'),
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    type_of_quiz = models.CharField(max_length=250, choices=TYPE_CHOICES, default='single')
    question = models.TextField(
        verbose_name=("Question"),
        blank=False)
    option_1 = models.TextField(
        verbose_name=("Type Option 1"),
        help_text=("Enetr option 1. This field has to be filled compulsorily."),
        blank=False)
    option_2 = models.TextField(
        verbose_name=("Type Option 2"),
        help_text=("Enter option 2. This field has to be filled compulsorily."),
        blank=True)
    option_3 = models.TextField(
        verbose_name=("Type Option 3"),
        help_text=("Enter option 3. If not required, then skip and leave the field blank."),
        default="",
        blank=True)
    option_4 = models.TextField(
        verbose_name=("Type Option 4"),
        help_text=("Enter option 4. If not required, then skip and leave the field blank."),
        default="",
        blank=True)
    option_5 = models.TextField(
        verbose_name=("Type Option 5"),
        help_text=("Enter option 5. If not required, then skip and leave the field blank."),
        default="",
        blank=True)
    answer = models.CharField(max_length=250, choices=ANSWER_CHOICES,  blank=True)
    answers = models.CharField(max_length=250, default="")
    level = models.CharField(max_length=250, null=False, blank=False, default="medium")

    def __str__(self):
        return self.question

class HardQuestionAnwers(models.Model):
    TYPE_CHOICES = [
    ('single', 'Single Correct Answer'),
    ('multiple', 'Multiple Correct Answers'),
    ]
    ANSWER_CHOICES = [
    ('1', 'Option 1'),
    ('2', 'Option 2'),
    ('3', 'Option 3'),
    ('4', 'Option 4'),
    ('5', 'Option 5'),
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    type_of_quiz = models.CharField(max_length=250, choices=TYPE_CHOICES, default='single')
    question = models.TextField(
        verbose_name=("Question"),
        blank=False)
    option_1 = models.TextField(
        verbose_name=("Type Option 1"),
        help_text=("Enetr option 1. This field has to be filled compulsorily."),
        blank=False)
    option_2 = models.TextField(
        verbose_name=("Type Option 2"),
        help_text=("Enter option 2. This field has to be filled compulsorily."),
        blank=True)
    option_3 = models.TextField(
        verbose_name=("Type Option 3"),
        help_text=("Enter option 3. If not required, then skip and leave the field blank."),
        default="",
        blank=True)
    option_4 = models.TextField(
        verbose_name=("Type Option 4"),
        help_text=("Enter option 4. If not required, then skip and leave the field blank."),
        default="",
        blank=True)
    option_5 = models.TextField(
        verbose_name=("Type Option 5"),
        help_text=("Enter option 5. If not required, then skip and leave the field blank."),
        default="",
        blank=True)
    answer = models.CharField(max_length=250, choices=ANSWER_CHOICES,  blank=True)
    answers = models.CharField(max_length=250, default="")
    level = models.CharField(max_length=250, null=False, blank=False, default="hard")

    def __str__(self):
        return self.question

class User_Detail(models.Model):
    STATUS_CHOICES = [
    ('pass', 'Pass'),
    ('fail', 'Fail'),
    ]
    name = models.CharField(
        verbose_name=("Name to be written on certificate"),
        max_length=250, blank=False, help_text=("Do ensure to not make spelling mistakes as certificates cannot be reissued."))
    email = models.EmailField(
        verbose_name = ("Email Id where certificate could be sent"),
        max_length=250, blank=False, help_text=("Do ensure to give proper email address without any errors."))
    attempted_at = models.DateTimeField(auto_now_add=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    marks_obtained = models.SmallIntegerField(
        null = True, blank=False, default=0)
    status = models.CharField(max_length=250,choices=STATUS_CHOICES, default='fail')

    def __str__(self):
        return self.email

class Entry(models.Model):
    duration = models.DurationField()