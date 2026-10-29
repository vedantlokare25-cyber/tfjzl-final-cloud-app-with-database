from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date')
    search_fields = ['name', 'description']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text']
    search_fields = ['question_text']

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'is_correct']

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
