from django.contrib import admin

from .models import Exam, OpenQuestion, OpenAnswer, UserExam


admin.site.register(Exam)
admin.site.register(OpenQuestion)
