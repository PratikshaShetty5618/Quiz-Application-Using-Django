from django.contrib import admin

from .models import *


# Register your models here.

# admin.site.register(CategoryManager)

admin.site.register(Category)

admin.site.register(Quiz)

admin.site.register(Same_Marking)

admin.site.register(Different_Marking)

admin.site.register(EasyQuestionAnwers)

admin.site.register(MediumQuestionAnwers)

admin.site.register(HardQuestionAnwers)

admin.site.register(User_Detail)