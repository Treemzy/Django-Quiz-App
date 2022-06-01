from django.contrib import admin
from .models import (Answer, Question, Student, StudentAnswer, Subject, User, TakenQuiz, Quiz, Profile)
# Register your models here.

# Register your models here.
admin.site.register(Answer)
admin.site.register(Student)
admin.site.register(StudentAnswer)
admin.site.register(Subject)
admin.site.register(User)
admin.site.register(Question)
admin.site.register(TakenQuiz)
admin.site.register(Quiz)
admin.site.register(Profile)

