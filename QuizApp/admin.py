from django.contrib import admin

from .models import Category,Quiz,Same_Marking,Different_Marking


# Register your models here.

# admin.site.register(CategoryManager)

admin.site.register(Category)

admin.site.register(Quiz)

admin.site.register(Same_Marking)

admin.site.register(Different_Marking)